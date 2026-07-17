@echo off
REM ════════════════════════════════════════════════════════════════════
REM  start_app.bat - Inicia la App Frontend Green-Ampt
REM  Uso: Ejecuta este archivo o escribe: start_app.bat
REM ════════════════════════════════════════════════════════════════════

cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          🌾 Green-Ampt Pro v2.0 - Aplicación Frontend           ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado o no está en PATH
    echo.
    echo Descarga Python desde: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.

REM Verificar dependencias
echo 📦 Verificando dependencias...
pip show flet >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Instalando dependencias...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error al instalar dependencias
        pause
        exit /b 1
    )
)

echo ✅ Dependencias OK
echo.

echo ════════════════════════════════════════════════════════════════════
echo  🚀 Iniciando Aplicación Frontend...
echo ════════════════════════════════════════════════════════════════════
echo.
echo ⚠️  IMPORTANTE:
echo   • Asegúrate de que el BACKEND está corriendo en otra terminal
echo   • python main.py
echo.
echo   • Si es la PRIMERA VEZ, edita config.py con tu IP local
echo   • python get_ip.py te ayudará a obtener tu IP
echo.

REM Ejecutar la app
python green_ampt_flet.py

REM Si la app falla
if errorlevel 1 (
    echo.
    echo ❌ Error al iniciar la aplicación
    pause
    exit /b 1
)
