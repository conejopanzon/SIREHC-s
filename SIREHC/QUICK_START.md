# ⚡ Guía Rápida - Sistema de Citas Médicas

## Instalación Rápida (3 pasos)

### 1️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2️⃣ Ejecutar la aplicación
```bash
python main.py
```

### 3️⃣ Iniciar sesión
- **Usuario:** `admin`
- **Contraseña:** `admin123`

---

## 🎯 Lo Primero que Debes Hacer

### Opción A: Como Administrador
```
1. Iniciar sesión con "admin"
2. Ir a "Crear Usuarios" para agregar más doctores
3. Asignar especialidades
```

### Opción B: Como Doctor
```
1. Iniciar sesión con "doctor"
2. Ir a "Registrar Paciente"
3. Luego "Agendar Cita Manual" o "Agendar Cita (IA)"
```

---

## 📱 Funciones Principales Explicadas

### 🔍 Buscar Paciente
- Encuentra pacientes registrados
- Visualiza su historial

### ➕ Registrar Paciente
- Llenar formulario con datos del paciente
- Agregar información de alergias y medicamentos

### 📅 Agendar Cita (Manual)
- Seleccionar doctor
- Elegir fecha/hora
- Agregar motivo de cita

### 🤖 Agendar Cita (IA)
- Describe síntomas
- La IA sugiere doctor especializado
- Confirma el agendamiento

### 📋 Gestionar Citas
- Ver todas las citas
- Editar o cancelar citas

---

## 🔧 Configuración Inicial

### Cambiar credenciales (Importante)
Edita `core/database.py` y busca las funciones de validación:

```python
# En database.py
def check_login(username, password):
    # Modificar aquí las credenciales
```

### Configurar API de OpenAI (Para IA)
Edita `services/ia_service.py`:

```python
# Agrega tu API key
OPENAI_API_KEY = "sk-your-key-here"
```

---

## ⌨️ Atajos Importantes

| Acción | Tecla |
|--------|-------|
| Enviar | `Enter` |
| Cerrar | `Esc` o botón X |

---

## 📊 Estructura de Datos

### Paciente
- Nombre, edad, email, teléfono
- Alergias, medicamentos

### Cita
- Paciente, doctor, fecha, hora
- Motivo, estado

### Doctor
- Nombre, especialidad
- Disponibilidad

---

## 🆘 Problemas Comunes

| Problema | Solución |
|----------|----------|
| Módulo no encontrado | `pip install -r requirements.txt` |
| BD bloqueada | Cierra la app y reinicia |
| Imagen no aparece | `python gui/assets/generate_medical_image.py` |
| Error de IA | Verifica API key en `services/ia_service.py` |

---

## 📞 ¿Necesitas ayuda?

1. Lee el `README.md` completo
2. Revisa la consola (errores/logs)
3. Verifica que Python 3.10+ esté instalado

---

**¡Listo para usar! 🚀**
