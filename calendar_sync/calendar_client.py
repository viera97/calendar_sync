"""
Google Calendar client for managing calendar operations.
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Optional, Dict, Any, Union
import logging
from .event import Event


class GoogleCalendarClient:
    """Client for interacting with Google Calendar API."""
    
    def __init__(self, service_account_file: str, calendar_id: str):
        """
        Initialize Google Calendar client.
        
        Args:
            service_account_file: Path to service account JSON file
            calendar_id: Google Calendar ID to work with
        """
        self.service_account_file = service_account_file
        self.calendar_id = calendar_id
        self.service: Optional[Any] = None
        self.logger = logging.getLogger(__name__)
        
        # Initialize the service
        self._initialize_service()
    
    def _initialize_service(self) -> None:
        """Initialize Google Calendar service with credentials."""
        try:
            # Load credentials
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_file,
                scopes=['https://www.googleapis.com/auth/calendar']
            )
            
            # Build the service
            self.service = build('calendar', 'v3', credentials=credentials)
            self.logger.info("Google Calendar service initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Google Calendar service: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test connection to Google Calendar API.
        
        Returns:
            True if connection is successful, False otherwise
        """
        if self.service is None:
            self.logger.error("Service not initialized")
            return False
            
        try:
            # Try to get calendar information
            calendar = self.service.calendars().get(calendarId=self.calendar_id).execute()
            self.logger.info(f"Successfully connected to calendar: {calendar.get('summary', 'Unknown')}")
            return True
            
        except HttpError as e:
            self.logger.error(f"HTTP error testing connection: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error testing connection: {e}")
            return False
    
    def create_event(self, event: Event) -> Optional[str]:
        """
        Create an event in Google Calendar.
        
        Args:
            event: Event object to create
            
        Returns:
            HTML link to the created event, or None if failed
        """
        if self.service is None:
            self.logger.error("Service not initialized")
            return None
            
        try:
            # Convert event to Google Calendar format
            event_data = event.to_google_calendar_format()
            
            # Create the event
            result = self.service.events().insert(
                calendarId=self.calendar_id, 
                body=event_data
            ).execute()
            
            # Store event details
            event.event_id = result.get('id')
            event.html_link = result.get('htmlLink')
            
            self.logger.info(f"Event created successfully: {event.title}")
            return event.html_link
            
        except HttpError as e:
            self.logger.error(f"HTTP error creating event: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error creating event: {e}")
            return None
    
    def get_events(self, time_min: Optional[str] = None, time_max: Optional[str] = None, max_results: int = 250) -> List[Dict[str, Any]]:
        """
        Get events from Google Calendar.
        
        Args:
            time_min: Lower bound for event start time (RFC3339 timestamp)
            time_max: Upper bound for event start time (RFC3339 timestamp)
            max_results: Maximum number of events to return
            
        Returns:
            List of event dictionaries
        """
        if self.service is None:
            self.logger.error("Service not initialized")
            return []
            
        try:
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            self.logger.info(f"Retrieved {len(events)} events")
            return events
            
        except HttpError as e:
            self.logger.error(f"HTTP error getting events: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error getting events: {e}")
            return []
    
    def update_event(self, event: Event) -> bool:
        """
        Update an existing event in Google Calendar.
        
        Args:
            event: Event object with updated information
            
        Returns:
            True if successful, False otherwise
        """
        if not event.event_id:
            self.logger.error("Cannot update event without event_id")
            return False
        
        if self.service is None:
            self.logger.error("Service not initialized")
            return False
        
        try:
            # Convert event to Google Calendar format
            event_data = event.to_google_calendar_format()
            
            # Update the event
            self.service.events().update(
                calendarId=self.calendar_id,
                eventId=event.event_id,
                body=event_data
            ).execute()
            
            self.logger.info(f"Event updated successfully: {event.title}")
            return True
            
        except HttpError as e:
            self.logger.error(f"HTTP error updating event: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error updating event: {e}")
            return False
    
    def delete_event(self, event_id: str) -> bool:
        """
        Delete an event from Google Calendar.
        
        Args:
            event_id: Google Calendar event ID
            
        Returns:
            True if successful, False otherwise
        """
        if self.service is None:
            self.logger.error("Service not initialized")
            return False
            
        try:
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            
            self.logger.info(f"Event deleted successfully: {event_id}")
            return True
            
        except HttpError as e:
            self.logger.error(f"HTTP error deleting event: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error deleting event: {e}")
            return False
    
    def get_calendar_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the calendar.
        
        Returns:
            Calendar information dictionary, or None if failed
        """
        if self.service is None:
            self.logger.error("Service not initialized")
            return None
            
        try:
            calendar = self.service.calendars().get(calendarId=self.calendar_id).execute()
            return calendar
            
        except HttpError as e:
            self.logger.error(f"HTTP error getting calendar info: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error getting calendar info: {e}")
            return None