"""
Tests for the Event classes.
"""

from datetime import datetime, timezone
from calendar_sync.event import Event, AppointmentEvent


class TestEvent:
    """Tests for the Event class."""
    
    def test_event_creation(self):
        """Test basic event creation."""
        start_time = datetime(2025, 10, 17, 10, 0, tzinfo=timezone.utc)
        end_time = datetime(2025, 10, 17, 11, 0, tzinfo=timezone.utc)
        
        event = Event(
            title="Test Event",
            start_time=start_time,
            end_time=end_time,
            description="Test description",
            location="Test location"
        )
        
        assert event.title == "Test Event"
        assert event.start_time == start_time
        assert event.end_time == end_time
        assert event.description == "Test description"
        assert event.location == "Test location"
        assert event.timezone == "America/Mexico_City"
    
    def test_event_to_google_format(self):
        """Test conversion to Google Calendar format."""
        start_time = datetime(2025, 10, 17, 10, 0, tzinfo=timezone.utc)
        end_time = datetime(2025, 10, 17, 11, 0, tzinfo=timezone.utc)
        
        event = Event(
            title="Test Event",
            start_time=start_time,
            end_time=end_time,
            description="Test description",
            location="Test location"
        )
        
        google_format = event.to_google_calendar_format()
        
        assert google_format['summary'] == "Test Event"
        assert google_format['description'] == "Test description"
        assert google_format['location'] == "Test location"
        assert 'start' in google_format
        assert 'end' in google_format
        assert google_format['start']['timeZone'] == "America/Mexico_City"
    
    def test_event_str_representation(self):
        """Test string representation of event."""
        start_time = datetime(2025, 10, 17, 10, 0, tzinfo=timezone.utc)
        end_time = datetime(2025, 10, 17, 11, 0, tzinfo=timezone.utc)
        
        event = Event("Test Event", start_time, end_time)
        expected = f"Test Event ({start_time} - {end_time})"
        
        assert str(event) == expected


class TestAppointmentEvent:
    """Tests for the AppointmentEvent class."""
    
    def test_appointment_creation(self):
        """Test appointment event creation."""
        start_time = datetime(2025, 10, 17, 14, 0, tzinfo=timezone.utc)
        end_time = datetime(2025, 10, 17, 15, 0, tzinfo=timezone.utc)
        
        appointment = AppointmentEvent(
            client_name="John Doe",
            phone_number="+1 555 123 4567",
            service_type="Haircut",
            start_time=start_time,
            end_time=end_time,
            additional_notes="First visit"
        )
        
        assert appointment.client_name == "John Doe"
        assert appointment.phone_number == "+1 555 123 4567"
        assert appointment.service_type == "Haircut"
        assert appointment.additional_notes == "First visit"
        assert appointment.title == "Appointment - John Doe"
        assert "APPOINTMENT INFORMATION" in appointment.description
    
    def test_appointment_description_format(self):
        """Test appointment description formatting."""
        start_time = datetime(2025, 10, 17, 14, 0, tzinfo=timezone.utc)
        end_time = datetime(2025, 10, 17, 15, 0, tzinfo=timezone.utc)
        
        appointment = AppointmentEvent(
            client_name="Jane Smith",
            phone_number="+1 555 987 6543",
            service_type="Manicure",
            start_time=start_time,
            end_time=end_time,
            additional_notes="Regular client"
        )
        
        description = appointment.description
        assert "Jane Smith" in description
        assert "+1 555 987 6543" in description
        assert "Manicure" in description
        assert "Regular client" in description
        assert "📋 APPOINTMENT INFORMATION" in description
    
    def test_appointment_google_format(self):
        """Test appointment Google Calendar format includes color."""
        start_time = datetime(2025, 10, 17, 14, 0, tzinfo=timezone.utc)
        end_time = datetime(2025, 10, 17, 15, 0, tzinfo=timezone.utc)
        
        appointment = AppointmentEvent(
            client_name="Test Client",
            phone_number="+1 555 000 0000",
            service_type="Test Service",
            start_time=start_time,
            end_time=end_time
        )
        
        google_format = appointment.to_google_calendar_format()
        
        assert google_format['colorId'] == '9'
        assert google_format['summary'] == "Appointment - Test Client"
    
    def test_update_notes(self):
        """Test updating appointment notes."""
        start_time = datetime(2025, 10, 17, 14, 0, tzinfo=timezone.utc)
        end_time = datetime(2025, 10, 17, 15, 0, tzinfo=timezone.utc)
        
        appointment = AppointmentEvent(
            client_name="Test Client",
            phone_number="+1 555 000 0000",
            service_type="Test Service",
            start_time=start_time,
            end_time=end_time,
            additional_notes="Original notes"
        )
        
        # Update notes
        appointment.update_notes("Updated notes")
        
        assert appointment.additional_notes == "Updated notes"
        assert "Updated notes" in appointment.description
        assert "Original notes" not in appointment.description