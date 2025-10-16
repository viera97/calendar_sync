"""
Main application file demonstrating the use of the calendar sync classes.
"""

import logging
from datetime import datetime, timedelta
from calendar_sync import GoogleCalendarClient, AppointmentEvent, AppointmentManager
from calendar_sync.config import CalendarConfig


def setup_logging(log_level: str = 'INFO') -> None:
    """
    Setup logging configuration.
    
    Args:
        log_level: Logging level
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('calendar_sync.log')
        ]
    )


def main():
    """Main application function."""
    # Load configuration
    config = CalendarConfig()
    
    # Validate configuration
    if not config.validate():
        print("Configuration validation failed. Please check your settings.")
        return
    
    # Setup logging
    setup_logging(config.log_level)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Calendar Sync Application")
    print(config)
    
    try:
        # Initialize Google Calendar client
        logger.info("Initializing Google Calendar client...")
        calendar_client = GoogleCalendarClient(
            service_account_file=config.service_account_file,
            calendar_id=config.calendar_id
        )
        
        # Test connection
        logger.info("Testing connection to Google Calendar...")
        if not calendar_client.test_connection():
            logger.error("Failed to connect to Google Calendar")
            print("❌ Failed to connect to Google Calendar")
            return
        
        print("✅ Successfully connected to Google Calendar")
        
        # Initialize appointment manager
        appointment_manager = AppointmentManager(calendar_client)
        
        # Example: Create a test appointment
        logger.info("Creating test appointment...")
        test_start = datetime.now() + timedelta(days=1)
        test_start = test_start.replace(hour=14, minute=0, second=0, microsecond=0)
        test_end = test_start + timedelta(hours=1)
        
        appointment_link = appointment_manager.create_appointment(
            client_name="John Doe",
            phone_number="+1 555 123 4567",
            service_type="Haircut and styling",
            start_time=test_start,
            end_time=test_end,
            additional_notes="First-time client, prefers early appointments."
        )
        
        if appointment_link:
            print(f"✅ Test appointment created successfully!")
            print(f"📅 Appointment link: {appointment_link}")
        else:
            print("❌ Failed to create test appointment")
        
        # Example: Get available slots for tomorrow
        logger.info("Getting available slots for tomorrow...")
        tomorrow = datetime.now() + timedelta(days=1)
        available_slots = appointment_manager.get_available_slots(
            date=tomorrow,
            slot_duration_minutes=config.default_appointment_duration,
            business_start_hour=config.business_start_hour,
            business_end_hour=config.business_end_hour
        )
        
        print(f"\n📅 Available slots for {tomorrow.strftime('%Y-%m-%d')}:")
        for slot in available_slots[:5]:  # Show first 5 slots
            print(f"   - {slot.strftime('%H:%M')}")
        
        if len(available_slots) > 5:
            print(f"   ... and {len(available_slots) - 5} more slots")
        
        # Example: Get appointments for today
        logger.info("Getting appointments for today...")
        today_appointments = appointment_manager.get_appointments_for_day(datetime.now())
        
        print(f"\n📋 Appointments for today: {len(today_appointments)}")
        for appointment in today_appointments:
            title = appointment.get('summary', 'No title')
            start_time = appointment.get('start', {}).get('dateTime', 'No time')
            print(f"   - {title} at {start_time}")
        
        logger.info("Application completed successfully")
        print("\n✅ Calendar Sync Application completed successfully!")
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"❌ Application error: {e}")


if __name__ == '__main__':
    main()