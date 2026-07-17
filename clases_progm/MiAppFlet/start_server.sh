#!/bin/bash
# ════════════════════════════════════════════════════════════════════════
#  start_server.sh - Inicia el Backend Green-Ampt
#  Uso: chmod +x start_server.sh && ./start_server.sh
# ════════════════════════════════════════════════════════════════════════

clear
echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║          🌾 Green-Ampt Pro v2.0 - Backend Servidor              ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python3 no está instalado"
    echo ""
    echo "Instala Python desde: https://www.python.org/downloads/"
    echo ""
    read -p "Presiona ENTER para salir..."
    exit 1
fi

echo "✅ Python detectado: $(python3 --version)"
echo ""

# Verificar dependencias
echo "📦 Verificando dependencias..."
python3 -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Instalando dependencias..."
    echo ""
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Error al instalar dependencias"
        read -p "Presiona ENTER para salir..."
        exit 1
    fi
fi

echo "✅ Dependencias OK"
echo ""

echo "════════════════════════════════════════════════════════════════════"
echo "  🚀 Iniciando Backend..."
echo "════════════════════════════════════════════════════════════════════"
echo ""

# Ejecutar el servidor
python3 main.py

# Si el servidor falla
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Error al iniciar el servidor"
    read -p "Presiona ENTER para salir..."
    exit 1
fi
