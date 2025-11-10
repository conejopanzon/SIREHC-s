@echo off
REM Ejecutor del Sistema de Citas Médicas
REM Inicia la aplicación con mejor manejo de errores

title Sistema de Gestión de Citas Médicas

echo ============================================
echo  Sistema de Gestión de Citas Médicas
echo ============================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado o no está en PATH
    pause
    exit /b 1
)

REM Verificar si existe main.py
if not exist "main.py" (
    echo ERROR: No se encuentra main.py
    echo Asegúrate de estar en la carpeta correcta
    pause
    exit /b 1
)

REM Ejecutar la aplicación
echo [*] Iniciando aplicación...
echo.

python main.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: La aplicación se cerró con un error
    echo Por favor, revisa la consola arriba para más detalles
    pause
    exit /b 1
)
