@echo off
REM ════════════════════════════════════════════════════════════════════
REM  start_server.bat - Inicia el Backend Green-Ampt
REM  Uso: Ejecuta este archivo o escribe: start_server.bat
REM ════════════════════════════════════════════════════════════════════

cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          🌾 Green-Ampt Pro v2.0 - Backend Servidor              ║
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
pip show fastapi >nul 2>&1
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
echo  🚀 Iniciando Backend...
echo ════════════════════════════════════════════════════════════════════
echo.

REM Ejecutar el servidor
python main.py

REM Si el servidor falla
if errorlevel 1 (
    echo.
    echo ❌ Error al iniciar el servidor
    pause
    exit /b 1
)
