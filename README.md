# 🎉 Calendar Sync API - FUNCIONANDO PERFECTAMENTE

Una API REST con FastAPI para gestión de citas de negocio integrada con Google Calendar.

## ✅ Estado: COMPLETAMENTE FUNCIONAL

Tu API está **100% operativa** y crea citas correctamente en Google Calendar.

## 🚀 Características

- 📅 **API REST Simple**: Solo crea citas cuando recibe datos (sin sincronización automática)
- � **Integración Google Calendar**: Conecta con tu calendario específico de negocio
- ⚙️ **Validación Automática**: Modelos Pydantic validan datos de entrada
- � **Documentación Automática**: Swagger UI en `/docs`
- � **Configuración .env**: Carga variables desde archivo de configuración
- �️ **Manejo de Errores**: Respuestas claras para errores de validación

## 📁 Estructura del Proyecto

```
calendar_sync/
├── 🌐 simple_api.py           # ⭐ ARCHIVO PRINCIPAL - API FastAPI
├── 📦 calendar_sync/          # Lógica de negocio
│   ├── calendar_client.py     # Cliente de Google Calendar
│   ├── event.py              # Modelos de eventos
│   ├── appointment_manager.py # Gestor de citas
│   └── config.py             # Configuración (.env)
├── 🔧 credentials.json        # Credenciales de Google (service account)
├── ⚙️ .env                   # Variables de configuración
├── 📋 requirements.txt       # Dependencias
└── 🧪 test_direct.py         # Test directo del módulo
```

## 🔧 Configuración Rápida

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar Google Calendar
1. Crear proyecto en [Google Cloud Console](https://console.cloud.google.com/)
2. Habilitar Google Calendar API
3. Crear service account y descargar `credentials.json`
4. Crear calendario específico en Google Calendar
5. Compartir el calendario con el email del service account
6. Copiar el Calendar ID

### 3. Configurar variables (.env)
```env
GOOGLE_SERVICE_ACCOUNT_FILE=credentials.json
GOOGLE_CALENDAR_ID=tu_calendar_id@group.calendar.google.com
BUSINESS_NAME=Mi Negocio
DEFAULT_TIMEZONE=America/Mexico_City
```

### 4. Ejecutar la API
```bash
python simple_api.py
```

## 🌐 Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|---------|-------------|
| `/` | GET | Información de la API |
| `/health` | GET | Estado de conexión a Google Calendar |
| `/appointments` | POST | **Crear nueva cita** |
| `/docs` | GET | Documentación Swagger automática |

## 📝 Crear una Cita

### Ejemplo de uso:
```bash
curl -X POST "http://localhost:8000/appointments" \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Juan Pérez",
    "phone_number": "+1234567890",
    "service_type": "Consulta",
    "start_time": "2025-10-17T14:00:00.000Z",
    "end_time": "2025-10-17T15:00:00.000Z",
    "additional_notes": "Primera consulta",
    "timezone": "America/Mexico_City"
  }'
```

### Respuesta exitosa:
```json
{
  "success": true,
  "message": "Appointment created successfully",
  "appointment_link": "https://calendar.google.com/event?eid=...",
  "client_name": "Juan Pérez",
  "service_type": "Consulta",
  "start_time": "2025-10-17T14:00:00",
  "end_time": "2025-10-17T15:00:00"
}
```

## 🧪 Probar la API

### Health Check:
```bash
curl http://localhost:8000/health
```

### Test Directo (sin API):
```bash
python test_direct.py
```

### Documentación Interactiva:
Visita: http://localhost:8000/docs

## ⚠️ Validaciones Automáticas

La API valida automáticamente:
- ✅ **Teléfonos**: Mínimo 10 dígitos
- ✅ **Fechas**: `end_time` debe ser después de `start_time`
- ✅ **Campos obligatorios**: Nombre, teléfono, servicio, fechas
- ✅ **Formato**: Fechas en formato ISO (2025-10-17T14:00:00.000Z)

## 🎯 ¿Cómo Funciona?

1. **Recibes datos** via POST a `/appointments`
2. **Validación automática** con Pydantic
3. **Conexión a Google Calendar** con service account
4. **Creación del evento** en tu calendario específico
5. **Respuesta con enlace** directo al evento creado

## 🏆 Estado del Proyecto

✅ **API Completamente Funcional**  
✅ **Citas creándose correctamente**  
✅ **Validaciones funcionando**  
✅ **Configuración .env corregida**  
✅ **Documentación automática**  
✅ **Lista para producción**  

---

## 🚀 Uso en Producción

Tu Calendar Sync API está **lista para usar**. Solo inicia el servidor y comienza a crear citas:

```bash
python simple_api.py
```

**¡Proyecto completado exitosamente!** 🎉