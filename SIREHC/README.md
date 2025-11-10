# 🏥 Sistema de Gestión de Citas Médicas

Un sistema completo de gestión de citas médicas con inteligencia artificial, desarrollado en Python con interfaz gráfica moderna.

---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Credenciales Predeterminadas](#credenciales-predeterminadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Funcionalidades Principales](#funcionalidades-principales)
- [Solución de Problemas](#solución-de-problemas)

---

## ✨ Características

✅ **Autenticación segura** - Login con roles de usuario (admin/doctor)  
✅ **Gestión de pacientes** - Registrar y buscar pacientes  
✅ **Agendar citas** - Dos métodos: manual e inteligencia artificial  
✅ **Gestión de citas** - Ver, editar y eliminar citas  
✅ **Gestión de doctores** - Administrar doctores y especialidades  
✅ **Panel de administración** - Crear nuevos usuarios  
✅ **Interfaz moderna** - Diseño limpio y profesional con CustomTkinter  
✅ **Base de datos** - SQLite integrada  

---

## 🔧 Requisitos

- **Python 3.10+**
- **Windows/Mac/Linux**

### Dependencias Python:
- `customtkinter` - Interface gráfica moderna
- `pillow` - Procesamiento de imágenes
- `openai` - API de inteligencia artificial
- `pandas` - Análisis de datos
- `matplotlib` - Gráficos
- `requests` - Llamadas HTTP

---

## 📥 Instalación

### 1. Clonar o descargar el proyecto
```bash
cd tu_ruta/hackaton
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

O instalar manualmente:
```bash
pip install customtkinter pillow openai pandas matplotlib requests
```

### 3. Inicializar la base de datos
La base de datos se crea automáticamente al ejecutar la aplicación por primera vez.

---

## ⏱️ Inicio rápido (Windows — ejecución rápida)

Sigue estos pasos si quieres ejecutar la aplicación de forma rápida en Windows (PowerShell). Incluye la opción recomendada con entorno virtual y alternativas más rápidas.

Opción A — Recomendado (PowerShell, entorno virtual):

1. Abre PowerShell y sitúate en la carpeta del proyecto:

```powershell
cd "C:\ruta\a\SIREHC"  # o navega a la carpeta del proyecto
```

2. Crear y activar un entorno virtual:

```powershell
python -m venv .venv
# Si PowerShell bloquea la activación por políticas, permite scripts solo para esta sesión:
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependencias e iniciar la aplicación:

```powershell
pip install -r requirements.txt
python main.py
```

Opción B — Inicio rápido sin entorno virtual (instalación global o --user):

```powershell
pip install -r requirements.txt --user
python main.py
```

Opción C — Usar los batch existentes (rápido en Windows):

```powershell
# Ejecuta el script de instalación (si lo necesitas) y luego el de ejecución
.\install.bat
.\run.bat
```

Nota sobre PowerShell y activación de venv
- Si al ejecutar `.\.venv\Scripts\Activate.ps1` recibes un error por la política de ejecución, ejecuta el comando `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force` (solo cambia la política para la sesión actual).

Configurar OpenAI (si usas la función IA)
- Puedes exportar la variable de entorno antes de ejecutar la app en PowerShell:

```powershell
$env:OPENAI_API_KEY = "tu_api_key_aqui"
python main.py
```

Otras notas rápidas
- Si quieres ver mensajes de error completos, ejecuta `python main.py` desde PowerShell para ver los logs en consola.
- Si la interfaz no carga imágenes, ejecuta `python gui/assets/generate_medical_image.py` para regenerarlas.


## 🚀 Uso

### Iniciar la aplicación
```bash
python main.py
```

### Primer acceso
1. Abre la aplicación
2. Verás la pantalla de login con imagen médica
3. Usa las credenciales predeterminadas:
   - **Usuario:** `admin`
   - **Contraseña:** `admin123`

---

## 🔐 Credenciales Predeterminadas

| Rol | Usuario | Contraseña | Acceso |
|-----|---------|-----------|--------|
| Admin | `admin` | `admin123` | Panel completo + crear usuarios |
| Doctor | `doctor` | `doctor123` | Gestión de citas y pacientes |

> ⚠️ **Importante:** Cambia las contraseñas en producción

---

## 📁 Estructura del Proyecto

```
hackaton/
├── main.py                    # Punto de entrada de la aplicación
├── README.md                  # Este archivo
├── requirements.txt           # Dependencias del proyecto
│
├── core/
│   ├── __init__.py
│   └── database.py           # Gestión de base de datos SQLite
│
├── gui/
│   ├── __init__.py
│   ├── login_window.py       # Pantalla de login
│   ├── app_window.py         # Ventana principal de la aplicación
│   └── assets/
│       ├── generate_medical_image.py  # Generador de imagen médica
│       └── medical_bg.png            # Imagen de fondo del login
│
├── services/
│   ├── __init__.py
│   ├── ia_service.py         # Integración con OpenAI para citas inteligentes
│   └── email_service.py      # Servicio de envío de emails
│
└── assets/
    └── icon.ico              # Icono de la aplicación
```

---

## 🎯 Funcionalidades Principales

### 1️⃣ **Buscar Paciente**
- Búsqueda rápida de pacientes por nombre o ID
- Vista de historial de citas
- Información de contacto y medicamentos

### 2️⃣ **Registrar Paciente**
- Formulario completo con validaciones
- Guardar información de contacto
- Asignar medicamentos y alergias

### 3️⃣ **Agendar Cita (Manual)**
- Seleccionar doctor y especialidad
- Elegir fecha y hora disponible
- Asignar motivo de consulta

### 4️⃣ **Agendar Cita (IA)**
- Sistema inteligente que sugiere doctores basado en síntomas
- Utiliza OpenAI para análisis de síntomas
- Proporciona recomendaciones automáticas
- **Requiere API key de OpenAI** (configurable en `services/ia_service.py`)

### 5️⃣ **Gestionar Citas**
- Vista general de todas las citas
- Filtrar por estado (programada, realizada, cancelada)
- Editar detalles de citas
- Cancelar citas

### 6️⃣ **Gestionar Doctores**
- Agregar nuevos doctores
- Asignar especialidades
- Ver disponibilidad
- Eliminar doctores

### 7️⃣ **Panel de Administración** (Solo Admin)
- Crear nuevos usuarios
- Asignar roles (admin/doctor)
- Gestionar permisos

---

## 🤖 Uso de la Función de IA

### Configurar OpenAI API Key

1. Abre `services/ia_service.py`
2. Busca la línea de configuración de API key
3. Reemplaza con tu clave de OpenAI:

```python
openai.api_key = "tu-api-key-aqui"
```

### Cómo funciona
1. Ve a "Agendar Cita (IA)"
2. Describe los síntomas del paciente
3. El sistema analiza y sugiere doctores especializados
4. Confirma el agendamiento

---

## 📊 Base de Datos

### Tablas principales

**usuarios**
- id, username, password, role, created_at

**pacientes**
- id, nombre, edad, email, telefono, alergias, medicamentos

**doctores**
- id, nombre, especialidad, disponibilidad, contacto

**citas**
- id, paciente_id, doctor_id, fecha, hora, motivo, estado

---

## ⌨️ Atajos de Teclado

| Acción | Tecla |
|--------|-------|
| Iniciar sesión | `Enter` |
| Buscar | `Ctrl+F` |
| Salir | `Ctrl+Q` o cerrar ventana |

---

## 🐛 Solución de Problemas

### Error: "No se encuentra customtkinter"
```bash
pip install customtkinter --upgrade
```

### Error: "Database locked"
- Cierra todas las instancias de la aplicación
- Elimina `clinic.db` y reinicia

### Error: "OpenAI API key invalid"
- Verifica tu clave en `services/ia_service.py`
- Asegúrate de tener créditos en tu cuenta OpenAI

### Error: "Imagen no se carga"
- Ejecuta el generador de imagen:
```bash
python gui/assets/generate_medical_image.py
```

### La aplicación es lenta
- Reduce la cantidad de citas cargadas
- Verifica tu conexión a internet
- Limpia la base de datos de citas antiguas

---

## 📞 Soporte

Si encuentras problemas:

1. Revisa este README
2. Verifica los logs de la consola
3. Asegúrate de tener todas las dependencias instaladas
4. Intenta reinstalar dependencias:
```bash
pip install -r requirements.txt --force-reinstall
```

---

## 📄 Licencia

Este proyecto es de uso educativo. Úsalo libremente en tus proyectos.

---

## 👨‍💻 Desarrollo

### Agregar nuevas funcionalidades

1. **Backend:** Añade funciones en `core/database.py`
2. **Frontend:** Crea nuevos frames en `gui/app_window.py`
3. **Servicios:** Extiende `services/` para nuevas integraciones

### Modificar tema/colores

Los colores principales están en:
- `gui/login_window.py` - Colores del login
- `gui/app_window.py` - Tema de la aplicación principal

Colores utilizados:
- Primary: `#1F6E78` (verde médico)
- Secondary: `#3B71CA` (azul)
- Accent: `#E74C3C` (rojo)
- Background: `#F5F5F5` (gris claro)

---

## 📈 Próximas Mejoras

- [ ] Exportar citas a PDF
- [ ] Recordatorios por email
- [ ] Reportes estadísticos
- [ ] Aplicación móvil
- [ ] Autenticación multi-factor
- [ ] Dashboard con gráficos

---

**¡Disfruta usando el Sistema de Gestión de Citas Médicas! 🏥**

*Última actualización: Noviembre 2025*
