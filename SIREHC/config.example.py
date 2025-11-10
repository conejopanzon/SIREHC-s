# Configuración del Sistema de Citas Médicas

## 🔐 OpenAI API Configuration
# Para usar la función de IA, necesitas una clave de API de OpenAI
# Obtén una en: https://platform.openai.com/api-keys

OPENAI_API_KEY = "sk-your-api-key-here"

## 🏥 Configuración de Base de Datos
DATABASE_NAME = "clinic.db"
DATABASE_PATH = "./core/"

## 🎨 Tema de la Aplicación
THEME_COLOR_PRIMARY = "#1F6E78"      # Verde médico (títulos, botones principales)
THEME_COLOR_SECONDARY = "#3B71CA"    # Azul (elementos secundarios)
THEME_COLOR_ACCENT = "#E74C3C"       # Rojo (alertas, errores)
THEME_COLOR_BACKGROUND = "#F5F5F5"   # Gris claro (fondo)
THEME_COLOR_SUCCESS = "#27AE60"      # Verde (éxito)
THEME_COLOR_WARNING = "#F39C12"      # Naranja (advertencias)

## 📧 Configuración de Email
ENABLE_EMAIL_NOTIFICATIONS = True
EMAIL_SENDER = "citas@hospital.com"
EMAIL_PASSWORD = "your-email-password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

## 📱 Configuración de Interfaz
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700
LOGIN_WINDOW_WIDTH = 900
LOGIN_WINDOW_HEIGHT = 550
THEME_MODE = "light"  # "light" o "dark"

## 🔑 Credenciales Predeterminadas
# IMPORTANTE: Cambiar en producción
DEFAULT_ADMIN_USER = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"
DEFAULT_DOCTOR_USER = "doctor"
DEFAULT_DOCTOR_PASSWORD = "doctor123"

## 🏥 Especialidades Disponibles
SPECIALTIES = [
    'Médico General',
    'Cardiología',
    'Dermatología',
    'Gastroenterología',
    'Neurólogo',
    'Traumatólogo',
    'Cirujano',
    'Pediatra',
    'Ginecólogo',
    'Oftalmólogo',
    'Urólogo',
    'Otorrinolaringólogo'
]

## ⏰ Configuración de Horarios
OFFICE_HOURS_START = 8      # 8:00 AM
OFFICE_HOURS_END = 18       # 6:00 PM
APPOINTMENT_DURATION = 30   # minutos
DAYS_AHEAD_BOOKING = 30     # días permitidos para agendar

## 🚨 Configuración de Seguridad
SESSION_TIMEOUT = 1800      # segundos (30 minutos)
PASSWORD_MIN_LENGTH = 6
ENABLE_TWO_FACTOR = False

## 📊 Configuración de Logs
ENABLE_LOGGING = True
LOG_FILE = "app.log"
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

## 🔄 Configuración de Sincronización
AUTO_BACKUP = True
BACKUP_INTERVAL = 3600      # segundos (1 hora)
BACKUP_PATH = "./backups/"
