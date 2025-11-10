# 📚 Guía de Mejores Prácticas

## 🔐 Seguridad

### 1. Cambiar Credenciales Predeterminadas
**MUY IMPORTANTE** - Las credenciales por defecto solo son para desarrollo:
```
admin / admin123
doctor / doctor123
```

Para cambiarlas:
1. Abre `core/database.py`
2. Busca la función `init_db()`
3. Modifica los valores de usuario y contraseña

### 2. Proteger la API Key de OpenAI
- **NUNCA** commits tu API key en Git
- Usa variables de entorno:
  ```python
  import os
  OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
  ```

### 3. Validación de Datos
- Siempre valida entrada de usuarios
- Usa SQL prepared statements
- Sanitiza datos antes de guardar

### 4. Copias de Seguridad
- Haz backup regular de `clinic.db`
- Considera usar SQLite en modo WAL para mejor concurrencia
- Almacena backups en lugar seguro

---

## 💡 Performance

### 1. Optimización de Consultas
```python
# ❌ Malo: Múltiples consultas
for paciente in pacientes:
    citas = db.get_citas(paciente.id)

# ✓ Bueno: Una sola consulta con JOIN
citas = db.get_all_citas_with_patients()
```

### 2. Lazy Loading
- Carga datos bajo demanda
- No cargues toda la BD al inicio
- Implementa paginación para listas largas

### 3. Caché
```python
# Cachear resultados de API
@cache.cached(timeout=3600)
def get_doctor_recommendations(symptoms):
    return ia_service.analyze(symptoms)
```

---

## 🎨 Interfaz de Usuario

### 1. Consistencia de Colores
- Usa los colores definidos en `config.py`
- Mantén la paleta consistente

### 2. Responsive Design
- Prueba en diferentes resoluciones
- Usa grid y weights en Tkinter

### 3. Accesibilidad
- Contraste de texto suficiente
- Soporta navegación por teclado
- Mensajes de error claros

---

## 📝 Código

### 1. Estructura de Commits
```
[feat] Agregar login con dos factores
[fix] Corregir error en búsqueda de pacientes
[docs] Actualizar README
[refactor] Mejorar estructura de database.py
```

### 2. Documentación de Código
```python
def schedule_appointment(patient_id, doctor_id, date, time):
    """
    Agenda una cita médica.
    
    Args:
        patient_id (int): ID del paciente
        doctor_id (int): ID del doctor
        date (str): Fecha en formato YYYY-MM-DD
        time (str): Hora en formato HH:MM
    
    Returns:
        bool: True si fue exitoso, False si no
    
    Raises:
        ValueError: Si los parámetros son inválidos
    """
    pass
```

### 3. Manejo de Errores
```python
# ❌ Malo
try:
    result = db.get_patient(patient_id)
except:
    print("Error")

# ✓ Bueno
try:
    result = db.get_patient(patient_id)
except sqlite3.DatabaseError as e:
    logger.error(f"Error en BD: {e}")
    show_error_dialog("No se pudo obtener el paciente")
except ValueError as e:
    logger.warning(f"Parámetro inválido: {e}")
```

---

## 🧪 Testing

### Test Unitarios
```python
# test_database.py
import unittest
from core import database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = database.Database(":memory:")
    
    def test_create_patient(self):
        result = self.db.create_patient("Juan", 30, "juan@email.com")
        self.assertIsNotNone(result)
```

### Test Manuales
- Prueba login con credenciales incorrectas
- Prueba agendamiento sin doctor disponible
- Prueba con BD vacía

---

## 🚀 Despliegue

### 1. Crear Ejecutable (Windows)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

### 2. Distribución
- Incluir `README.md` y `requirements.txt`
- Crear carpeta `backups/` antes de entregar
- Documentar credenciales predeterminadas

### 3. Actualización
- Versionamiento semántico: `1.0.0`
- Changelog en `CHANGELOG.md`
- Migraciones de BD si hay cambios

---

## 📊 Monitoreo

### 1. Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### 2. Métricas
- Cantidad de citas por doctor
- Tasa de cancelación
- Tiempo promedio de citas

### 3. Alertas
- Cuando se acaban los turnos
- Error en API de OpenAI
- BD corrupta o no accesible

---

## 🔄 Mantenimiento Regular

### Semanal
- ✓ Revisar logs
- ✓ Backup manual

### Mensual
- ✓ Actualizar dependencias
- ✓ Revisar performance
- ✓ Cleanup de citas viejas

### Trimestral
- ✓ Auditoría de seguridad
- ✓ Revisión de código
- ✓ Pruebas completas

---

## 📚 Recursos Útiles

- [CustomTkinter Docs](https://customtkinter.com/)
- [SQLite Docs](https://www.sqlite.org/docs.html)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Python Best Practices](https://pep8.org/)

---

**Siguiente nivel: Implementa estas prácticas y tu sistema será robusto y profesional! 🚀**
