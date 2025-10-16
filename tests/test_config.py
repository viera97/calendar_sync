"""
Tests for the CalendarConfig class.
"""

import os
import tempfile
from unittest.mock import patch
from calendar_sync.config import CalendarConfig


class TestCalendarConfig:
    """Tests for the CalendarConfig class."""
    
    def test_default_configuration(self):
        """Test default configuration values."""
        config = CalendarConfig()
        
        assert config.service_account_file == 'credentials.json'
        assert config.calendar_id == 'primary'
        assert config.business_name == 'My Business'
        assert config.default_timezone == 'America/Mexico_City'
        assert config.business_start_hour == 9
        assert config.business_end_hour == 18
        assert config.default_appointment_duration == 60
        assert config.log_level == 'INFO'
    
    @patch.dict(os.environ, {
        'GOOGLE_SERVICE_ACCOUNT_FILE': 'test_credentials.json',
        'GOOGLE_CALENDAR_ID': 'test_calendar@group.calendar.google.com',
        'BUSINESS_NAME': 'Test Business',
        'DEFAULT_TIMEZONE': 'UTC',
        'BUSINESS_START_HOUR': '8',
        'BUSINESS_END_HOUR': '20',
        'DEFAULT_APPOINTMENT_DURATION': '30',
        'LOG_LEVEL': 'DEBUG'
    })
    def test_environment_configuration(self):
        """Test configuration from environment variables."""
        config = CalendarConfig()
        
        assert config.service_account_file == 'test_credentials.json'
        assert config.calendar_id == 'test_calendar@group.calendar.google.com'
        assert config.business_name == 'Test Business'
        assert config.default_timezone == 'UTC'
        assert config.business_start_hour == 8
        assert config.business_end_hour == 20
        assert config.default_appointment_duration == 30
        assert config.log_level == 'DEBUG'
    
    def test_validation_with_existing_file(self):
        """Test validation with existing service account file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
            tmp_file.write('{"test": "data"}')
            tmp_file_path = tmp_file.name
        
        try:
            with patch.dict(os.environ, {'GOOGLE_SERVICE_ACCOUNT_FILE': tmp_file_path}):
                config = CalendarConfig()
                assert config.validate() is True
        finally:
            # Clean up
            os.unlink(tmp_file_path)
    
    def test_validation_with_missing_file(self):
        """Test validation with missing service account file."""
        with patch.dict(os.environ, {'GOOGLE_SERVICE_ACCOUNT_FILE': 'nonexistent.json'}):
            config = CalendarConfig()
            assert config.validate() is False
    
    def test_validation_invalid_business_hours(self):
        """Test validation with invalid business hours."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
            tmp_file.write('{"test": "data"}')
            tmp_file_path = tmp_file.name
        
        try:
            with patch.dict(os.environ, {
                'GOOGLE_SERVICE_ACCOUNT_FILE': tmp_file_path,
                'BUSINESS_START_HOUR': '18',
                'BUSINESS_END_HOUR': '9'
            }):
                config = CalendarConfig()
                assert config.validate() is False
        finally:
            os.unlink(tmp_file_path)
    
    def test_validation_invalid_duration(self):
        """Test validation with invalid appointment duration."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
            tmp_file.write('{"test": "data"}')
            tmp_file_path = tmp_file.name
        
        try:
            with patch.dict(os.environ, {
                'GOOGLE_SERVICE_ACCOUNT_FILE': tmp_file_path,
                'DEFAULT_APPOINTMENT_DURATION': '0'
            }):
                config = CalendarConfig()
                assert config.validate() is False
        finally:
            os.unlink(tmp_file_path)
    
    def test_string_representation(self):
        """Test string representation of configuration."""
        config = CalendarConfig()
        config_str = str(config)
        
        assert "Calendar Configuration:" in config_str
        assert config.service_account_file in config_str
        assert config.business_name in config_str
        assert str(config.business_start_hour) in config_str