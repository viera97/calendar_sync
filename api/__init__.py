"""
API package for Calendar Sync.
"""

# Import models for easy access
from .models import (
    AppointmentCreate,
    AppointmentResponse, 
    HealthResponse,
    ErrorResponse
)

__all__ = [
    "AppointmentCreate",
    "AppointmentResponse",
    "HealthResponse", 
    "ErrorResponse"
]