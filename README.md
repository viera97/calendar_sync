# Calendar Sync API

A professional FastAPI-based REST API for business appointment management integrated with Google Calendar.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Google Calendar](https://img.shields.io/badge/Google%20Calendar-API-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- � **Simple REST API**: On-demand appointment creation (no automatic synchronization)
- 📅 **Google Calendar Integration**: Direct integration with your business calendar
- ⚡ **Automatic Validation**: Pydantic models with comprehensive data validation
- 📖 **Auto Documentation**: Interactive Swagger UI at `/docs`
- 🔧 **Environment Configuration**: Secure `.env` file configuration
- 🛡️ **Error Handling**: Clear error responses and comprehensive logging
- 🎯 **Production Ready**: CORS support, proper HTTP status codes, and exception handling

## 🏗️ Project Structure

```
calendar_sync/
├── simple_api.py             # 🌟 Main FastAPI application
├── calendar_sync/            # 📦 Business logic package
│   ├── __init__.py
│   ├── calendar_client.py    # Google Calendar client
│   ├── event.py             # Event models
│   ├── appointment_manager.py # Appointment business logic
│   └── config.py            # Configuration management
├── api/                      # 🔧 Alternative API structure
│   ├── __init__.py
│   ├── main.py
│   └── models.py
├── tests/                    # 🧪 Unit tests
│   ├── test_event.py
│   └── test_config.py
├── credentials.json          # Google service account credentials
├── .env                      # Environment variables
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
└── run_api.py              # Alternative API runner
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Cloud Console account
- Google Calendar API enabled

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/your-username/calendar_sync.git
cd calendar_sync

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Google Calendar Setup

1. **Create a Google Cloud Project**
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Create Service Account**
    - Go to: `IAM & Admin` -> `Service Accounts` -> `Create Service Account`.  
    - Click on +: 
      - Nombre: calendar-writer
      - ID: calendar-writer
      - Descripción: Opcional

3. **Download Json**
    - Click on created account and go to: `Keys` -> `Add Key` -> `Create new key`
    - Select: `JSON` -> `Create`

4. **Share google calendar**
    - Go to Google Calendar, click on side panel: `Settings and shareing` -> `Share with specific people`
    - Add the service account email, you can find it on the downloaded json with the format:
    ```
    calendar-writer@tu-proyecto.iam.gserviceaccount.com
    ```
    - Give permission: `Make changes to events`
    
### 3. Environment Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
GOOGLE_SERVICE_ACCOUNT_FILE=credentials.json
GOOGLE_CALENDAR_ID=your_calendar_id@group.calendar.google.com
BUSINESS_NAME=Your Business Name
DEFAULT_TIMEZONE=America/New_York
```

### 4. Run the API

```bash
python simple_api.py
```

The API will be available at:
- **Main API**: http://127.0.0.1:8000
- **Interactive Docs**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health

## 📋 API Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/` | GET | API information and status | None |
| `/health` | GET | Health check and Google Calendar connectivity | None |
| `/appointments` | POST | **Create new appointment** | None |
| `/docs` | GET | Interactive API documentation | None |

## 📝 Usage Examples

### Create an Appointment

```bash
curl -X POST "http://127.0.0.1:8000/appointments" \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "John Doe",
    "phone_number": "+1234567890",
    "service_type": "Business Consultation",
    "start_time": "2025-10-25T14:00:00.000Z",
    "end_time": "2025-10-25T15:00:00.000Z",
    "additional_notes": "First-time client consultation",
    "timezone": "America/New_York"
  }'
```

### Successful Response

```json
{
  "success": true,
  "message": "Appointment created successfully",
  "appointment_link": "https://calendar.google.com/event?eid=...",
  "client_name": "John Doe",
  "service_type": "Business Consultation",
  "start_time": "2025-10-25T14:00:00",
  "end_time": "2025-10-25T15:00:00"
}
```

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

```json
{
  "status": "healthy",
  "message": "API is healthy and connected to Google Calendar",
  "timestamp": "2025-10-24T20:30:00",
  "version": "1.0.0"
}
```

## 🔍 Data Validation

The API automatically validates:

- ✅ **Phone Numbers**: Minimum 10 digits required
- ✅ **Time Logic**: `end_time` must be after `start_time`
- ✅ **Required Fields**: Client name, phone, service type, and timestamps
- ✅ **Date Format**: ISO 8601 format (YYYY-MM-DDTHH:MM:SS.000Z)
- ✅ **String Lengths**: Appropriate limits for all text fields

## 🧪 Testing

### Run Unit Tests

```bash
pytest tests/ -v
```

### Test API Directly

```bash
python test_direct.py
```

### Interactive Testing

Visit http://127.0.0.1:8000/docs for the interactive Swagger UI where you can test all endpoints directly in your browser.

## 🔧 Configuration Options

| Environment Variable | Description | Default | Required |
|---------------------|-------------|---------|----------|
| `GOOGLE_SERVICE_ACCOUNT_FILE` | Path to Google service account JSON | `credentials.json` | Yes |
| `GOOGLE_CALENDAR_ID` | Google Calendar ID | None | Yes |
| `BUSINESS_NAME` | Your business name | `Calendar Sync` | No |
| `DEFAULT_TIMEZONE` | Default timezone for appointments | `UTC` | No |

## 🚨 Error Handling

The API provides comprehensive error handling with clear HTTP status codes:

- **200 OK**: Successful operations
- **201 Created**: Appointment created successfully
- **400 Bad Request**: Invalid request data
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server-side errors
- **503 Service Unavailable**: Google Calendar connection issues

## �️ Architecture

The application follows clean architecture principles:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   Business       │    │   Google        │
│   (REST API)    │───▶│   Logic          │───▶│   Calendar API  │
│                 │    │   (Appointments) │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌──────────────────┐
│   Pydantic      │    │   Configuration  │
│   (Validation)  │    │   (.env files)   │
└─────────────────┘    └──────────────────┘
```

## 🚀 Production Deployment

### Security Considerations

- Keep `credentials.json` secure and never commit to version control
- Use environment variables for all sensitive configuration
- Consider implementing API authentication for production use
- Review and configure CORS settings appropriately

### Performance

- The API is stateless and can be easily scaled horizontally
- Google Calendar API has rate limits - consider implementing request throttling for high-traffic scenarios
- Monitor Google Calendar quota usage

### Monitoring

- Check `/health` endpoint for system monitoring
- Review application logs for errors and performance metrics
- Monitor Google Calendar API quota and usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [documentation](http://127.0.0.1:8000/docs) when the API is running
2. Review the health check endpoint at `/health`
3. Check the application logs for detailed error information
4. Open an issue in the repository for bugs or feature requests

---