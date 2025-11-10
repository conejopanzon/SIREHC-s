# 📖 Índice de Documentación

Bienvenido al Sistema de Gestión de Citas Médicas. Aquí encontrarás toda la documentación disponible.

---

## 🚀 Empezar Rápido

### Para usuarios nuevos:
1. **[QUICK_START.md](QUICK_START.md)** - Guía de instalación y uso básico (3 pasos)
2. **[install.bat](install.bat)** - Instalador automático para Windows
3. **[run.bat](run.bat)** - Script para ejecutar la aplicación

---

## 📚 Documentación Principal

### [README.md](README.md) ⭐ **LEER PRIMERO**
Documentación completa con:
- Características de la aplicación
- Requisitos del sistema
- Instalación detallada
- Instrucciones de uso completas
- Estructura del proyecto
- Configuración de OpenAI
- Solución de problemas

**Tiempo de lectura:** 10-15 minutos

---

## 🎓 Guías Específicas

### [BEST_PRACTICES.md](BEST_PRACTICES.md)
Para desarrolladores que quieran mejorar el código:
- Seguridad (cambiar contraseñas, proteger API keys)
- Performance y optimización
- Mejores prácticas de código
- Testing
- Deployment
- Monitoreo

**Público:** Desarrolladores/Mantenedores

---

### [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
Solución de problemas común:
- Problemas de instalación
- Problemas de ejecución
- Problemas de base de datos
- Problemas de interfaz gráfica
- Problemas de IA/OpenAI
- Problemas de performance

**Público:** Todos (especialmente usuarios con problemas)

---

## ⚙️ Configuración

### [config.example.py](config.example.py)
Archivo de configuración de ejemplo con todos los parámetros disponibles:
- OpenAI API key
- Temas de color
- Horarios de oficina
- Seguridad
- Logging
- Y más...

**Cómo usar:**
```bash
cp config.example.py config.py
# Edita config.py con tus valores
```

---

## 📋 Archivos de Instalación

| Archivo | Sistema | Descripción |
|---------|---------|-------------|
| [install.bat](install.bat) | Windows | Instalador automático |
| [run.bat](run.bat) | Windows | Script para ejecutar la app |
| [requirements.txt](requirements.txt) | Todos | Dependencias Python |

---

## 📁 Estructura del Proyecto

```
hackaton/
├── 📄 README.md                 ← LEE ESTO PRIMERO
├── 📄 QUICK_START.md            ← Instalación rápida
├── 📄 BEST_PRACTICES.md         ← Para desarrolladores
├── 📄 TROUBLESHOOTING.md        ← Solución de problemas
├── 📄 INDEX.md                  ← Este archivo
├── 📄 config.example.py         ← Configuración de ejemplo
├── 📄 requirements.txt           ← Dependencias
├── 📄 install.bat               ← Instalador Windows
├── 📄 run.bat                   ← Ejecutor Windows
├── 🐍 main.py                   ← Punto de entrada
│
├── 📁 core/
│   ├── database.py              ← Base de datos SQLite
│   └── clinic.db                ← BD (se crea automáticamente)
│
├── 📁 gui/
│   ├── login_window.py          ← Pantalla de login
│   ├── app_window.py            ← Aplicación principal
│   └── assets/
│       ├── generate_medical_image.py  ← Generador de imagen
│       └── medical_bg.png            ← Imagen de fondo
│
└── 📁 services/
    ├── ia_service.py            ← Integración con OpenAI
    └── email_service.py         ← Servicio de emails
```

---

## 🎯 Rutas de Aprendizaje Recomendadas

### Ruta 1: Instalar y Usar (Usuario Final)
1. Lee [QUICK_START.md](QUICK_START.md) (5 min)
2. Ejecuta `install.bat` (5 min)
3. Ejecuta `run.bat` (inmediato)
4. Consulta [README.md](README.md) si tienes preguntas

**Tiempo total:** 15 minutos

---

### Ruta 2: Instalar y Configurar (Administrador)
1. Lee [QUICK_START.md](QUICK_START.md)
2. Ejecuta `install.bat`
3. Lee [README.md](README.md) - sección "Configuración"
4. Lee [BEST_PRACTICES.md](BEST_PRACTICES.md)
5. Personaliza `config.example.py` → `config.py`

**Tiempo total:** 30-45 minutos

---

### Ruta 3: Desarrollo y Mejora (Programador)
1. Lee todo el [README.md](README.md)
2. Estudia [BEST_PRACTICES.md](BEST_PRACTICES.md)
3. Revisa la estructura del código en `core/`, `gui/`, `services/`
4. Consulta [TROUBLESHOOTING.md](TROUBLESHOOTING.md) si hay problemas
5. Implementa nuevas funcionalidades

**Tiempo total:** 2-3 horas

---

### Ruta 4: Solucionar Problemas (User con Errores)
1. Busca tu problema en [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Sigue los pasos de solución
3. Si persiste, consulta [README.md](README.md) - sección relevante
4. Ejecuta `install.bat` nuevamente si es necesario

**Tiempo variable:** 5-30 minutos

---

## 🔍 Búsqueda Rápida

### ¿Cómo inicio la aplicación?
→ Ver [QUICK_START.md](QUICK_START.md)

### ¿Cuál es la contraseña predeterminada?
→ Ver [README.md](README.md) - Credenciales Predeterminadas

### ¿Cómo configuro OpenAI?
→ Ver [README.md](README.md) - Uso de la Función de IA

### Tengo error al instalar
→ Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problemas de Instalación

### La aplicación va lenta
→ Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problemas de Rendimiento

### Quiero mejorar el código
→ Ver [BEST_PRACTICES.md](BEST_PRACTICES.md)

### La BD se perdió
→ Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problemas de Base de Datos

---

## 💡 Tips Útiles

### Primer acceso
```bash
# Usuario: admin
# Contraseña: admin123
```

### Crear ejecutable (Windows)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

### Hacer backup de datos
```bash
# Windows
copy core\clinic.db backups\clinic_backup.db

# Mac/Linux
cp core/clinic.db backups/clinic_backup.db
```

### Limpiar ambiente
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt --upgrade
```

---

## 📞 Contacto y Soporte

Si necesitas ayuda:

1. **Primero:** Consulta [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. **Luego:** Lee [README.md](README.md) completamente
3. **Si persiste:** Reúne información:
   - Versión de Python: `python --version`
   - SO: Windows/Mac/Linux
   - Error exacto (copia completo)
   - Pasos para reproducir

---

## 📊 Información del Proyecto

- **Nombre:** Sistema de Gestión de Citas Médicas
- **Versión:** 1.0.0
- **Tipo:** Aplicación de Escritorio (Desktop)
- **Framework:** CustomTkinter
- **BD:** SQLite
- **IA:** OpenAI GPT
- **Lenguaje:** Python 3.10+
- **Licencia:** Educativo

---

## ✅ Checklist de Inicio

- [ ] Versión de Python 3.10+
- [ ] Instaladas todas las dependencias (`pip install -r requirements.txt`)
- [ ] Base de datos inicializada (automático al ejecutar)
- [ ] Imagen médica generada (automático)
- [ ] API key de OpenAI (solo si usas IA)
- [ ] Credenciales cambiadas (recomendado para producción)

---

## 🎉 ¡Estás Listo!

Sigue la ruta recomendada para tu caso de uso y estarás operativo en minutos.

**¿Preguntas?** → Consulta el índice arriba o busca en [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

*Documentación completa actualizada a Noviembre 2025*
