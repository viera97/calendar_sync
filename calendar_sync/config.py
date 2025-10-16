"""
Configuration settings for the calendar sync application.
"""

import os
from typing import Optional


class CalendarConfig:
    """Configuration class for calendar settings."""
    
    def __init__(self):
        """Initialize configuration with environment variables or defaults."""
        # Google Calendar settings
        self.service_account_file = self._get_env('GOOGLE_SERVICE_ACCOUNT_FILE', 'credentials.json')
        self.calendar_id = self._get_env('GOOGLE_CALENDAR_ID', 'primary')
        
        # Business settings
        self.business_name = self._get_env('BUSINESS_NAME', 'My Business')
        self.default_timezone = self._get_env('DEFAULT_TIMEZONE', 'America/Mexico_City')
        self.business_start_hour = int(self._get_env('BUSINESS_START_HOUR', '9'))
        self.business_end_hour = int(self._get_env('BUSINESS_END_HOUR', '18'))
        self.default_appointment_duration = int(self._get_env('DEFAULT_APPOINTMENT_DURATION', '60'))
        
        # Logging settings
        self.log_level = self._get_env('LOG_LEVEL', 'INFO')
        self.log_file = self._get_env('LOG_FILE', 'calendar_sync.log')
    
    def _get_env(self, key: str, default: str) -> str:
        """
        Get environment variable with default fallback.
        
        Args:
            key: Environment variable key
            default: Default value if not found
            
        Returns:
            Environment variable value or default
        """
        return os.getenv(key, default)
    
    def validate(self) -> bool:
        """
        Validate configuration settings.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        if not os.path.exists(self.service_account_file):
            print(f"Error: Service account file not found: {self.service_account_file}")
            return False
        
        if self.business_start_hour >= self.business_end_hour:
            print("Error: Business start hour must be before end hour")
            return False
        
        if self.default_appointment_duration <= 0:
            print("Error: Default appointment duration must be positive")
            return False
        
        return True
    
    def __str__(self) -> str:
        """String representation of configuration."""
        return f"""Calendar Configuration:
- Service Account File: {self.service_account_file}
- Calendar ID: {self.calendar_id}
- Business Name: {self.business_name}
- Timezone: {self.default_timezone}
- Business Hours: {self.business_start_hour}:00 - {self.business_end_hour}:00
- Default Appointment Duration: {self.default_appointment_duration} minutes
- Log Level: {self.log_level}"""