"""
Calendar Sync Package

A Python package for managing calendar appointments and events.
"""

from .calendar_client import GoogleCalendarClient
from .event import Event, AppointmentEvent
from .appointment_manager import AppointmentManager

__version__ = "1.0.0"
__author__ = "Dayron Viera"

__all__ = [
    "GoogleCalendarClient",
    "Event", 
    "AppointmentEvent",
    "AppointmentManager"
]