#!/bin/bash
# ════════════════════════════════════════════════════════════════════════
#  start_app.sh - Inicia la App Frontend Green-Ampt
#  Uso: chmod +x start_app.sh && ./start_app.sh
# ════════════════════════════════════════════════════════════════════════

clear
echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║          🌾 Green-Ampt Pro v2.0 - Aplicación Frontend           ║"
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
python3 -c "import flet" 2>/dev/null
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
echo "  🚀 Iniciando Aplicación Frontend..."
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   • Asegúrate de que el BACKEND está corriendo en otra terminal"
echo "   • python3 main.py"
echo ""
echo "   • Si es la PRIMERA VEZ, edita config.py con tu IP local"
echo "   • python3 get_ip.py te ayudará a obtener tu IP"
echo ""

# Ejecutar la app
python3 green_ampt_flet.py

# Si la app falla
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Error al iniciar la aplicación"
    read -p "Presiona ENTER para salir..."
    exit 1
fi
