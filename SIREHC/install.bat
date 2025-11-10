@echo off
REM Instalador del Sistema de Citas Médicas
REM Compatible con Windows

echo ============================================
echo  Sistema de Gestión de Citas Médicas
echo  Instalador Automático
echo ============================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado o no está en PATH
    echo Descarga Python desde: https://www.python.org/
    pause
    exit /b 1
)

echo [✓] Python detectado
echo.

REM Mostrar versión de Python
echo Versión de Python:
python --version
echo.

REM Instalar dependencias
echo [*] Instalando dependencias...
echo.

pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Fallo al instalar dependencias
    pause
    exit /b 1
)

echo.
echo [✓] Dependencias instaladas correctamente
echo.

REM Generar imagen médica
echo [*] Generando imagen médica...
python gui\assets\generate_medical_image.py

if %errorlevel% neq 0 (
    echo.
    echo WARNING: No se pudo generar la imagen médica
    echo Continuando con la instalación...
    echo.
) else (
    echo [✓] Imagen médica generada
    echo.
)

REM Información final
echo ============================================
echo  Instalación Completada!
echo ============================================
echo.
echo Para iniciar la aplicación, ejecuta:
echo    python main.py
echo.
echo Credenciales predeterminadas:
echo    Usuario: admin
echo    Contraseña: admin123
echo.
echo Lee el archivo README.md para más información
echo.
pause
