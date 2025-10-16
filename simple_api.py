"""
Simple API server for Calendar Sync.
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

import logging
from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
import re

# Import our local modules
from calendar_sync import GoogleCalendarClient, AppointmentManager
from calendar_sync.config import CalendarConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models directly in this file to avoid import issues
class AppointmentCreate(BaseModel):
    """Model for creating a new appointment."""
    
    client_name: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Name of the client"
    )
    phone_number: str = Field(
        ..., 
        min_length=10, 
        max_length=20,
        description="Client's phone number"
    )
    service_type: str = Field(
        ..., 
        min_length=1, 
        max_length=200,
        description="Type of service requested"
    )
    start_time: datetime = Field(
        ...,
        description="Appointment start time in ISO format"
    )
    end_time: datetime = Field(
        ...,
        description="Appointment end time in ISO format"
    )
    additional_notes: Optional[str] = Field(
        default="",
        max_length=500,
        description="Additional notes for the appointment"
    )
    timezone: Optional[str] = Field(
        default="UTC",
        description="Timezone for the appointment"
    )
    
    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v):
        """Validate phone number format."""
        digits_only = re.sub(r'[^\d]', '', v)
        if len(digits_only) < 10:
            raise ValueError('Phone number must have at least 10 digits')
        return v
    
    @field_validator('end_time')
    @classmethod
    def validate_end_time(cls, v, info):
        """Validate that end_time is after start_time."""
        if hasattr(info, 'data') and 'start_time' in info.data:
            start_time = info.data['start_time']
            if v <= start_time:
                raise ValueError(f'End time ({v}) must be after start time ({start_time})')
        return v


class AppointmentResponse(BaseModel):
    """Model for appointment response."""
    
    success: bool = Field(..., description="Whether the appointment was created successfully")
    message: str = Field(..., description="Success or error message")
    appointment_link: Optional[str] = Field(default=None, description="Google Calendar event link")
    client_name: Optional[str] = Field(default=None, description="Name of the client")
    service_type: Optional[str] = Field(default=None, description="Type of service")
    start_time: Optional[datetime] = Field(default=None, description="Appointment start time")
    end_time: Optional[datetime] = Field(default=None, description="Appointment end time")


class HealthResponse(BaseModel):
    """Model for health check response."""
    
    status: str = Field(..., description="API status")
    message: str = Field(..., description="Health check message")
    timestamp: datetime = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")


class ErrorResponse(BaseModel):
    """Model for error responses."""
    
    success: bool = Field(default=False, description="Always false for errors")
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")


# Create FastAPI application
app = FastAPI(
    title="Calendar Sync API",
    description="Simple API for creating business appointments in Google Calendar",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_calendar_client() -> GoogleCalendarClient:
    """Get a calendar client instance."""
    try:
        config = CalendarConfig()
        logger.info(f"🔧 API Config - Service Account: {config.service_account_file}")
        logger.info(f"🔧 API Config - Calendar ID: {config.calendar_id}")
        
        if not config.validate():
            raise ValueError("Invalid configuration")
        
        client = GoogleCalendarClient(
            service_account_file=config.service_account_file,
            calendar_id=config.calendar_id
        )
        return client
    except Exception as e:
        logger.error(f"Failed to create calendar client: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to initialize Google Calendar client: {str(e)}"
        )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred"
        ).model_dump()
    )


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the API is running and can connect to Google Calendar"
)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    try:
        client = get_calendar_client()
        calendar_status = client.test_connection()
        
        status_message = (
            "API is healthy and connected to Google Calendar" 
            if calendar_status 
            else "API is running but Google Calendar connection failed"
        )
        
        return HealthResponse(
            status="healthy" if calendar_status else "degraded",
            message=status_message,
            timestamp=datetime.now(),
            version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            message=f"Health check failed: {str(e)}",
            timestamp=datetime.now(),
            version="1.0.0"
        )


@app.post(
    "/appointments",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Appointment",
    description="Create a new appointment in Google Calendar"
)
async def create_appointment(appointment_data: AppointmentCreate) -> AppointmentResponse:
    """Create a new appointment."""
    try:
        logger.info(f"Creating appointment for {appointment_data.client_name}")
        
        # Additional validation
        if appointment_data.end_time <= appointment_data.start_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"End time ({appointment_data.end_time}) must be after start time ({appointment_data.start_time})"
            )
        
        # Get calendar client
        client = get_calendar_client()
        
        # Create appointment manager
        manager = AppointmentManager(client)
        
        # Create the appointment
        appointment_link = manager.create_appointment(
            client_name=appointment_data.client_name,
            phone_number=appointment_data.phone_number,
            service_type=appointment_data.service_type,
            start_time=appointment_data.start_time,
            end_time=appointment_data.end_time,
            additional_notes=appointment_data.additional_notes or "",
            timezone=appointment_data.timezone or "UTC"
        )
        
        if appointment_link:
            logger.info(f"Appointment created successfully for {appointment_data.client_name}")
            
            return AppointmentResponse(
                success=True,
                message="Appointment created successfully",
                appointment_link=appointment_link,
                client_name=appointment_data.client_name,
                service_type=appointment_data.service_type,
                start_time=appointment_data.start_time,
                end_time=appointment_data.end_time
            )
        else:
            logger.error(f"Failed to create appointment for {appointment_data.client_name}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create appointment in Google Calendar"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating appointment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating appointment: {str(e)}"
        )


@app.get(
    "/",
    summary="Root Endpoint",
    description="Welcome message and API information"
)
async def root() -> Dict[str, Any]:
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Calendar Sync API",
        "description": "Simple API for creating business appointments",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "create_appointment": "POST /appointments",
            "health_check": "GET /health"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("simple_api:app", host="127.0.0.1", port=8000, reload=True)