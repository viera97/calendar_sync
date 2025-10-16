"""
Pydantic models for the Calendar Sync API.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re


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
        default="America/Mexico_City",
        description="Timezone for the appointment"
    )
    
    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v):
        """Validate phone number format."""
        # Remove all non-digit characters for validation
        digits_only = re.sub(r'[^\d]', '', v)
        if len(digits_only) < 10:
            raise ValueError('Phone number must have at least 10 digits')
        return v
    
    @field_validator('start_time')
    @classmethod
    def validate_start_time(cls, v):
        """Validate that start_time is not in the past."""
        if v < datetime.now():
            raise ValueError('Start time cannot be in the past')
        return v

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        json_schema_extra = {
            "example": {
                "client_name": "John Doe",
                "phone_number": "+1 555 123 4567",
                "service_type": "Haircut and styling",
                "start_time": "2025-10-17T14:00:00",
                "end_time": "2025-10-17T15:00:00",
                "additional_notes": "Client prefers short haircut",
                "timezone": "America/Mexico_City"
            }
        }


class AppointmentResponse(BaseModel):
    """Model for appointment response."""
    
    success: bool = Field(
        ...,
        description="Whether the appointment was created successfully"
    )
    message: str = Field(
        ...,
        description="Success or error message"
    )
    appointment_link: Optional[str] = Field(
        default=None,
        description="Google Calendar link to the created appointment"
    )
    appointment_id: Optional[str] = Field(
        default=None,
        description="Google Calendar event ID"
    )
    client_name: Optional[str] = Field(
        default=None,
        description="Name of the client"
    )
    service_type: Optional[str] = Field(
        default=None,
        description="Type of service"
    )
    start_time: Optional[datetime] = Field(
        default=None,
        description="Appointment start time"
    )
    end_time: Optional[datetime] = Field(
        default=None,
        description="Appointment end time"
    )
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Appointment created successfully",
                "appointment_link": "https://calendar.google.com/calendar/event?eid=...",
                "appointment_id": "abc123def456",
                "client_name": "John Doe",
                "service_type": "Haircut and styling",
                "start_time": "2025-10-17T14:00:00",
                "end_time": "2025-10-17T15:00:00"
            }
        }


class HealthResponse(BaseModel):
    """Model for health check response."""
    
    status: str = Field(..., description="API status")
    message: str = Field(..., description="Health check message")
    timestamp: datetime = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ErrorResponse(BaseModel):
    """Model for error responses."""
    
    success: bool = Field(default=False, description="Always false for errors")
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[dict] = Field(default=None, description="Additional error details")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "ValidationError",
                "message": "Invalid input data",
                "details": {
                    "field": "phone_number",
                    "error": "Phone number must have at least 10 digits"
                }
            }
        }