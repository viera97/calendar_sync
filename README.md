# Calendar Sync

A Python application for managing business appointments and calendar synchronization with Google Calendar.

## Features

- 📅 **Appointment Management**: Create, view, and manage business appointments
- 🔗 **Google Calendar Integration**: Seamless integration with Google Calendar API
- 🏢 **Business-Focused**: Designed specifically for business appointment scheduling
- 🛠️ **Object-Oriented Architecture**: Clean, maintainable code structure
- ⚙️ **Configurable**: Flexible configuration through environment variables
- 📊 **Availability Checking**: Find available time slots automatically
- 📝 **Detailed Logging**: Comprehensive logging for debugging and monitoring

## Project Structure

```
calendar_sync/
├── calendar_sync/              # Main package
│   ├── __init__.py            # Package initialization
│   ├── calendar_client.py     # Google Calendar API client
│   ├── event.py               # Event and appointment classes
│   ├── appointment_manager.py # Business appointment management
│   └── config.py              # Configuration management
├── main.py                    # Main application entry point
├── calendar_app.py            # Legacy simple script (for reference)
├── requirements.txt           # Python dependencies
├── .env.example              # Configuration template
└── README.md                 # This file
```

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd calendar_sync
```

2. **Create and activate virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Setup configuration**:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Google Calendar Setup

1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one

2. **Enable Calendar API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Calendar API" and enable it

3. **Create Service Account**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Download the JSON credentials file
   - Rename it to `credentials.json` and place in project root

4. **Share Calendar**:
   - Open Google Calendar
   - Create a new calendar for your business
   - Share it with the service account email (from credentials.json)
   - Copy the calendar ID and update it in your `.env` file

## Configuration

Edit the `.env` file with your settings:

```ini
# Google Calendar Configuration
GOOGLE_SERVICE_ACCOUNT_FILE=credentials.json
GOOGLE_CALENDAR_ID=your_calendar_id@group.calendar.google.com

# Business Configuration
BUSINESS_NAME=My Business
DEFAULT_TIMEZONE=America/Mexico_City
BUSINESS_START_HOUR=9
BUSINESS_END_HOUR=18
DEFAULT_APPOINTMENT_DURATION=60

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=calendar_sync.log
```

## Usage

### Quick Start

```bash
python main.py
```

### Using the Classes

```python
from calendar_sync import GoogleCalendarClient, AppointmentManager
from calendar_sync.config import CalendarConfig
from datetime import datetime, timedelta

# Load configuration
config = CalendarConfig()

# Initialize calendar client
calendar_client = GoogleCalendarClient(
    service_account_file=config.service_account_file,
    calendar_id=config.calendar_id
)

# Create appointment manager
appointment_manager = AppointmentManager(calendar_client)

# Create a new appointment
appointment_link = appointment_manager.create_appointment(
    client_name="John Doe",
    phone_number="+1 555 123 4567",
    service_type="Consultation",
    start_time=datetime.now() + timedelta(days=1, hours=2),
    end_time=datetime.now() + timedelta(days=1, hours=3),
    additional_notes="First-time client"
)

print(f"Appointment created: {appointment_link}")
```

### Creating Simple Events

```python
from calendar_sync import GoogleCalendarClient
from calendar_sync.event import Event
from datetime import datetime, timedelta

# Create a simple event
event = Event(
    title="Team Meeting",
    start_time=datetime.now() + timedelta(hours=2),
    end_time=datetime.now() + timedelta(hours=3),
    description="Weekly team sync meeting"
)

# Create in calendar
calendar_client = GoogleCalendarClient('credentials.json', 'calendar_id')
event_link = calendar_client.create_event(event)
```

## API Reference

### GoogleCalendarClient

Main class for interacting with Google Calendar API.

**Methods:**
- `test_connection()` - Test connection to Google Calendar
- `create_event(event)` - Create an event in the calendar
- `get_events(time_min, time_max)` - Get events from calendar
- `update_event(event)` - Update an existing event
- `delete_event(event_id)` - Delete an event

### AppointmentManager

High-level manager for business appointments.

**Methods:**
- `create_appointment()` - Create a new business appointment
- `get_appointments_for_day(date)` - Get appointments for specific day
- `get_appointments_for_week(start_date)` - Get appointments for week
- `get_available_slots(date)` - Find available time slots
- `cancel_appointment(event_id)` - Cancel an appointment

### Event Classes

- `Event` - Base event class
- `AppointmentEvent` - Specialized class for business appointments

## Development

### Running Tests

```bash
python -m pytest tests/ -v
```

### Code Formatting

```bash
black calendar_sync/ main.py
flake8 calendar_sync/ main.py
mypy calendar_sync/ main.py
```

## Troubleshooting

### Common Issues

1. **"Service account not found"**
   - Make sure `credentials.json` exists in the project root
   - Verify the service account has Calendar API access

2. **"Calendar not found"**
   - Check that the calendar ID is correct
   - Ensure the calendar is shared with the service account email

3. **"Permission denied"**
   - Verify the service account has appropriate permissions
   - Check that the Calendar API is enabled in Google Cloud Console

## License

MIT License

## Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request