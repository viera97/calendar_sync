"""
FastAPI application for Calendar Sync API.
Simple API that creates appointments on demand.
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from calendar_sync import GoogleCalendarClient, AppointmentManager
from calendar_sync.config import CalendarConfig
from api.models import AppointmentCreate, AppointmentResponse, HealthResponse, ErrorResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_calendar_client() -> GoogleCalendarClient:
    """Get a calendar client instance."""
    try:
        config = CalendarConfig()
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