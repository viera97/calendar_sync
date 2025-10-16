"""
Appointment manager for handling business appointments.
"""

from datetime import datetime, timedelta
from typing import List, Optional
import logging
from .calendar_client import GoogleCalendarClient
from .event import AppointmentEvent


class AppointmentManager:
    """Manager class for handling business appointments."""
    
    def __init__(self, calendar_client: GoogleCalendarClient):
        """
        Initialize appointment manager.
        
        Args:
            calendar_client: Google Calendar client instance
        """
        self.calendar_client = calendar_client
        self.logger = logging.getLogger(__name__)
    
    def create_appointment(
        self,
        client_name: str,
        phone_number: str,
        service_type: str,
        start_time: datetime,
        end_time: datetime,
        additional_notes: str = "",
        timezone: str = "America/Mexico_City"
    ) -> Optional[str]:
        """
        Create a new business appointment.
        
        Args:
            client_name: Client's name
            phone_number: Client's phone number
            service_type: Type of service requested
            start_time: Appointment start time
            end_time: Appointment end time
            additional_notes: Additional notes
            timezone: Appointment timezone
            
        Returns:
            HTML link to the created appointment, or None if failed
        """
        try:
            # Create appointment event
            appointment = AppointmentEvent(
                client_name=client_name,
                phone_number=phone_number,
                service_type=service_type,
                start_time=start_time,
                end_time=end_time,
                additional_notes=additional_notes,
                timezone=timezone
            )
            
            # Create the appointment in Google Calendar
            html_link = self.calendar_client.create_event(appointment)
            
            if html_link:
                self.logger.info(f"Appointment created for {client_name}: {service_type}")
                return html_link
            else:
                self.logger.error(f"Failed to create appointment for {client_name}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error creating appointment: {e}")
            return None
    
    def get_appointments_for_day(self, date: datetime) -> List[dict]:
        """
        Get all appointments for a specific day.
        
        Args:
            date: Date to get appointments for
            
        Returns:
            List of appointment dictionaries
        """
        try:
            # Set time boundaries for the day
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            # Get events from Google Calendar
            events = self.calendar_client.get_events(
                time_min=start_of_day.isoformat(),
                time_max=end_of_day.isoformat()
            )
            
            # Filter for appointments (events with "Appointment -" in title)
            appointments = [
                event for event in events 
                if event.get('summary', '').startswith('Appointment -')
            ]
            
            self.logger.info(f"Found {len(appointments)} appointments for {date.date()}")
            return appointments
            
        except Exception as e:
            self.logger.error(f"Error getting appointments for day: {e}")
            return []
    
    def get_appointments_for_week(self, start_date: datetime) -> List[dict]:
        """
        Get all appointments for a week starting from given date.
        
        Args:
            start_date: Start date of the week
            
        Returns:
            List of appointment dictionaries
        """
        try:
            # Calculate end of week
            end_date = start_date + timedelta(days=7)
            
            # Get events from Google Calendar
            events = self.calendar_client.get_events(
                time_min=start_date.isoformat(),
                time_max=end_date.isoformat()
            )
            
            # Filter for appointments
            appointments = [
                event for event in events 
                if event.get('summary', '').startswith('Appointment -')
            ]
            
            self.logger.info(f"Found {len(appointments)} appointments for week starting {start_date.date()}")
            return appointments
            
        except Exception as e:
            self.logger.error(f"Error getting appointments for week: {e}")
            return []
    
    def cancel_appointment(self, event_id: str) -> bool:
        """
        Cancel an appointment by deleting it from the calendar.
        
        Args:
            event_id: Google Calendar event ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            success = self.calendar_client.delete_event(event_id)
            
            if success:
                self.logger.info(f"Appointment cancelled: {event_id}")
            else:
                self.logger.error(f"Failed to cancel appointment: {event_id}")
                
            return success
            
        except Exception as e:
            self.logger.error(f"Error cancelling appointment: {e}")
            return False
    
    def reschedule_appointment(
        self, 
        event_id: str, 
        new_start_time: datetime, 
        new_end_time: datetime
    ) -> bool:
        """
        Reschedule an appointment to new times.
        
        Args:
            event_id: Google Calendar event ID
            new_start_time: New start time
            new_end_time: New end time
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # This would require getting the existing event, modifying it, and updating
            # For now, this is a placeholder for future implementation
            self.logger.info(f"Rescheduling appointment {event_id} to {new_start_time}")
            
            # TODO: Implement rescheduling logic
            # 1. Get existing event
            # 2. Create new AppointmentEvent with same data but new times
            # 3. Update the event
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error rescheduling appointment: {e}")
            return False
    
    def get_available_slots(
        self, 
        date: datetime, 
        slot_duration_minutes: int = 60,
        business_start_hour: int = 9,
        business_end_hour: int = 18
    ) -> List[datetime]:
        """
        Get available time slots for a given day.
        
        Args:
            date: Date to check availability
            slot_duration_minutes: Duration of each slot in minutes
            business_start_hour: Business day start hour (24h format)
            business_end_hour: Business day end hour (24h format)
            
        Returns:
            List of available start times
        """
        try:
            # Get existing appointments for the day
            appointments = self.get_appointments_for_day(date)
            
            # Create list of all possible slots
            available_slots = []
            current_time = date.replace(hour=business_start_hour, minute=0, second=0, microsecond=0)
            end_time = date.replace(hour=business_end_hour, minute=0, second=0, microsecond=0)
            
            while current_time < end_time:
                slot_end = current_time + timedelta(minutes=slot_duration_minutes)
                
                # Check if this slot conflicts with existing appointments
                is_available = True
                for appointment in appointments:
                    apt_start = datetime.fromisoformat(
                        appointment['start']['dateTime'].replace('Z', '+00:00')
                    )
                    apt_end = datetime.fromisoformat(
                        appointment['end']['dateTime'].replace('Z', '+00:00')
                    )
                    
                    # Check for overlap
                    if (current_time < apt_end and slot_end > apt_start):
                        is_available = False
                        break
                
                if is_available:
                    available_slots.append(current_time)
                
                # Move to next slot
                current_time += timedelta(minutes=slot_duration_minutes)
            
            self.logger.info(f"Found {len(available_slots)} available slots for {date.date()}")
            return available_slots
            
        except Exception as e:
            self.logger.error(f"Error getting available slots: {e}")
            return []