# 🔧 Troubleshooting - Solución de Problemas

## Tabla de Contenidos
- [Problemas de Instalación](#problemas-de-instalación)
- [Problemas de Ejecución](#problemas-de-ejecución)
- [Problemas de Base de Datos](#problemas-de-base-de-datos)
- [Problemas de Interfaz](#problemas-de-interfaz)
- [Problemas de IA](#problemas-de-ia)
- [Problemas de Rendimiento](#problemas-de-rendimiento)

---

## Problemas de Instalación

### ❌ "Python is not recognized as an internal or external command"

**Causa:** Python no está en el PATH

**Soluciones:**
1. Reinstala Python y marca "Add Python to PATH" durante instalación
2. O agrega manualmente a PATH:
   - Windows: `Panneau Control > Variables de entorno > Editar variables de entorno del sistema`
   - Agrega la ruta de Python (ej: `C:\Users\tu_usuario\AppData\Local\Programs\Python\Python313`)

3. Verifica:
   ```bash
   python --version
   ```

---

### ❌ "No module named 'customtkinter'"

**Causa:** Dependencias no instaladas

**Solución:**
```bash
pip install customtkinter pillow openai pandas matplotlib requests numpy
```

O mejor aún:
```bash
pip install -r requirements.txt
```

**Si sigue fallando:**
```bash
pip uninstall customtkinter
pip install customtkinter --upgrade
```

---

### ❌ "Could not find a version that satisfies the requirement"

**Causa:** Tu versión de Python es muy antigua

**Solución:**
```bash
python --version  # Verifica tu versión
pip install --upgrade pip
pip install -r requirements.txt
```

Requiere Python 3.10+. Si tienes versión menor, actualiza Python.

---

### ❌ "Permission denied" o "Access denied"

**Causa:** Permisos insuficientes

**Solución:**
- **Windows:** Ejecuta PowerShell como Administrador:
  ```bash
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

- **Mac/Linux:**
  ```bash
  sudo pip install -r requirements.txt
  ```

---

## Problemas de Ejecución

### ❌ La aplicación no inicia

**Causa:** Error en `main.py`

**Solución:**
1. Verifica que estés en la carpeta correcta:
   ```bash
   cd tu_ruta/hackaton
   pwd  # o "cd" en Windows para verificar
   ```

2. Ejecuta con output detallado:
   ```bash
   python -u main.py
   ```

3. Busca el error en la consola y anota línea/mensaje

---

### ❌ "ModuleNotFoundError" al iniciar

**Causa:** Falta algún módulo

**Solución:**
```bash
# Instalación completa
pip install customtkinter pillow openai pandas matplotlib requests

# O regenerar ambiente
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

---

### ❌ Ventana aparecer pero se cierra inmediatamente

**Causa:** Error durante la inicialización

**Solución:**
1. Ejecuta sin interfaz gráfica:
   ```bash
   python -u main.py 2>&1 | tee output.log
   ```

2. Lee el archivo `output.log` para ver errores

3. Típicamente es error en `database.py`:
   ```bash
   python -c "from core import database; database.init_db()"
   ```

---

## Problemas de Base de Datos

### ❌ "database is locked"

**Causa:** La BD está siendo accedida por otra instancia

**Soluciones:**

1. **Rápido:** Cierra todas las ventanas de la app y reinicia

2. **Nuclear:** Elimina la BD (perderás datos):
   ```bash
   rm clinic.db  # Mac/Linux
   del clinic.db  # Windows
   ```
   Luego reinicia la app para crear nueva BD

3. **Mejor:** Revisa si hay proceso Python corriendo:
   ```bash
   # Windows
   tasklist | findstr python
   
   # Mac/Linux
   ps aux | grep python
   ```
   Mata el proceso:
   ```bash
   taskkill /PID 12345 /F  # Windows
   kill -9 12345           # Mac/Linux
   ```

---

### ❌ "no such table: patients"

**Causa:** BD no inicializada correctamente

**Solución:**
```bash
python -c "from core import database; database.init_db()"
```

Luego reinicia la app.

---

### ❌ Datos desaparecen después de cerrar

**Causa:** BD guardada en lugar incorrecto

**Verificación:**
```bash
# Busca clinic.db
find . -name "clinic.db"  # Mac/Linux
dir /s clinic.db          # Windows
```

La BD debe estar en: `core/clinic.db`

---

### ❌ "database disk image is malformed"

**Causa:** BD corrupta

**Solución (pierde datos):**
```bash
# Backup primero si es posible
cp clinic.db clinic.db.backup

# Luego elimina y recrea
rm clinic.db
python -c "from core import database; database.init_db()"
```

---

## Problemas de Interfaz

### ❌ Imagen no se muestra en login

**Causa:** `medical_bg.png` falta o en lugar incorrecto

**Solución:**
```bash
# Regenera la imagen
python gui/assets/generate_medical_image.py

# Verifica que exista
ls gui/assets/medical_bg.png        # Mac/Linux
dir gui\assets\medical_bg.png       # Windows
```

---

### ❌ Ventana deformada o elementos mal colocados

**Causa:** Resolución de pantalla diferente

**Soluciones:**

1. Edita `gui/login_window.py` y `gui/app_window.py`:
   ```python
   # Cambia estos valores a tu resolución
   self.geometry("900x550")  # Ancho x Alto
   ```

2. O ajusta automáticamente:
   ```python
   self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
   ```

---

### ❌ Texto muy pequeño o muy grande

**Causa:** DPI de pantalla diferente

**Solución:**
Edita los tamaños de fuente en los archivos `.py`:
```python
# Cambiar
font=ctk.CTkFont(size=20, weight="bold")

# Por
font=ctk.CTkFont(size=14, weight="bold")  # Más pequeño
font=ctk.CTkFont(size=24, weight="bold")  # Más grande
```

---

### ❌ Los botones no responden

**Causa:** La aplicación está procesando

**Soluciones:**

1. Espera unos segundos (especialmente para IA)

2. Si está completamente congelada:
   ```bash
   taskkill /PID 12345 /F  # Windows
   killall python           # Mac/Linux
   ```

3. Revisa si hay llamada a OpenAI bloqueante:
   - Implementa threading en `ia_service.py`

---

## Problemas de IA

### ❌ "openai.error.AuthenticationError"

**Causa:** API key de OpenAI inválida o falta

**Solución:**

1. Obtén clave en: https://platform.openai.com/api-keys

2. Agrega en `services/ia_service.py`:
   ```python
   import openai
   openai.api_key = "sk-your-api-key-here"
   ```

3. Prueba:
   ```bash
   python -c "import openai; openai.api_key='sk-...'; print(openai.Model.list())"
   ```

---

### ❌ "RateLimitError: Rate limit exceeded"

**Causa:** Superaste el límite de API calls

**Soluciones:**

1. Espera 1 minuto antes de reintentar

2. Implementa espera:
   ```python
   import time
   time.sleep(60)  # Espera 60 segundos
   ```

3. Implementa caché para evitar llamadas duplicadas

4. Usa modelo más barato: `gpt-3.5-turbo` en lugar de `gpt-4`

---

### ❌ "No response from API"

**Causa:** Problema de conexión a internet

**Solución:**

1. Verifica conexión:
   ```bash
   ping google.com
   ```

2. Verifica que OpenAI no esté caído:
   - https://status.openai.com/

3. Reintentar la operación

---

### ❌ La IA da respuestas incorrectas

**Causa:** El prompt no es claro

**Solución:**
Edita el prompt en `services/ia_service.py`:
```python
prompt = """
Eres un asistente médico. El paciente reporta:
[síntomas]

Sugiere los 3 especialistas más apropiados.
"""
```

Mejora la descripción de síntomas solicitada al usuario.

---

## Problemas de Rendimiento

### ❌ Aplicación lenta

**Causa:** Muchos registros, conexión lenta a BD

**Soluciones:**

1. Implementa paginación:
   ```python
   # Cargar solo 50 registros por página
   def get_appointments(page=1, limit=50):
       offset = (page - 1) * limit
       # SQL: LIMIT 50 OFFSET offset
   ```

2. Agrega índices en `database.py`:
   ```python
   CREATE INDEX idx_patient_id ON appointments(patient_id)
   CREATE INDEX idx_date ON appointments(appointment_date)
   ```

3. Limpia datos viejos:
   ```python
   DELETE FROM appointments WHERE appointment_date < DATE('now', '-1 year')
   ```

---

### ❌ Respuestas de IA muy lentas

**Causa:** Modelo lento o problema de conexión

**Soluciones:**

1. Usa modelo más rápido:
   ```python
   # Cambiar en ia_service.py
   model = "gpt-3.5-turbo"  # Más rápido
   # En lugar de
   model = "gpt-4"  # Más lento pero mejor
   ```

2. Implementa threading:
   ```python
   from threading import Thread
   
   def get_recommendation_async(symptoms, callback):
       thread = Thread(target=lambda: callback(get_recommendation(symptoms)))
       thread.start()
   ```

3. Implementa timeout:
   ```python
   import signal
   signal.alarm(10)  # 10 segundos máximo
   ```

---

### ❌ Mucho uso de memoria RAM

**Causa:** Muchos datos cargados simultáneamente

**Soluciones:**

1. No cargues todo al inicio:
   ```python
   # ❌ Malo
   self.all_appointments = db.get_all()
   
   # ✓ Bueno
   self.appointments = db.get_appointments(limit=50)
   ```

2. Limpia referencias:
   ```python
   del large_variable
   gc.collect()  # Liberar memoria
   ```

3. Usa generadores:
   ```python
   def get_appointments_generator():
       for appointment in db.get_all():
           yield appointment
   ```

---

## 📞 Si Nada Funciona

1. **Reinstala completamente:**
   ```bash
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt --upgrade
   ```

2. **Crea ambiente limpio:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Recompila la imagen:**
   ```bash
   python gui/assets/generate_medical_image.py
   ```

4. **Elimina base de datos:**
   ```bash
   rm core/clinic.db  # Mae/Linux
   del core\clinic.db  # Windows
   ```

5. **Reinicia todo y ejecuta:**
   ```bash
   python main.py
   ```

---

## 📝 Reporte de Errores

Si el problema persiste, crea un reporte:

1. **Qué versión de Python:**
   ```bash
   python --version
   ```

2. **Qué error exacto aparece:** (copia todo el mensaje)

3. **En qué paso falla:** (instalación, ejecución, feature específico)

4. **Qué SO usas:** (Windows/Mac/Linux)

5. **Pasos para reproducir:**
   ```
   1. Abrí la app
   2. Hice clic en "Agendar Cita"
   3. Error: ...
   ```

---

**¡Espero que encuentres la solución! 🚀 Si no, pide ayuda proporcionando esta información.**
