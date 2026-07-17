# ══════════════════════════════════════════════════════════════════════════
#  config.py — Configuración flexible para Green-Ampt App
#  ✅ Funciona en: WiFi Local, WiFi Diferente, Datos Móviles (con Ngrok)
# ══════════════════════════════════════════════════════════════════════════

# ┌──────────────────────────────────────────────────────────────────────┐
# │  CÓMO OBTENER TU IP LOCAL:                                           │
# │                                                                      │
# │  📍 WINDOWS:                                                         │
# │     Abre CMD y escribe:  ipconfig                                    │
# │     Busca: "IPv4 Address" → algo como 192.168.x.x                   │
# │                                                                      │
# │  📍 MAC/LINUX:                                                       │
# │     Abre Terminal y escribe:  hostname -I  o  ifconfig              │
# │     Busca: algo como 192.168.x.x o 10.0.x.x                         │
# │                                                                      │
# │  📍 PARA NGROK (Datos Móviles):                                      │
# │     1. Descarga: https://ngrok.com/download                          │
# │     2. Abre CMD/Terminal en la carpeta de ngrok                      │
# │     3. Ejecuta: ngrok http 8001                                      │
# │     4. Copia la URL que aparece (ej: https://xxxx-xx.ngrok-free.app)│
# │                                                                      │
# └──────────────────────────────────────────────────────────────────────┘

# ╔════════════════════════════════════════════════════════════════════╗
# ║  📝 CONFIGURA ESTOS VALORES:                                       ║
# ╚════════════════════════════════════════════════════════════════════╝

# Opción 1: WiFi Local (PC y celular en misma red)
LOCAL_PC_IP = "192.168.50.155"          # ← REEMPLAZA CON TU IP REAL

# Opción 2: Datos Móviles (Necesita Ngrok)
NGROK_URL = "https://xxxx-xxxx-xxxx.ngrok-free.app"  # ← URL de Ngrok

# Puerto del servidor (debe coincidir en main.py)
PORT = 8001

# Ambiente por defecto (se puede cambiar desde la app)
ENVIRONMENT = "device"  # Opciones: "device" (WiFi), "ngrok" (Datos móviles)

# ══════════════════════════════════════════════════════════════════════════
# 🚫 NO EDITES DEBAJO DE ESTA LÍNEA
# ══════════════════════════════════════════════════════════════════════════

_URLS = {
    "emulator": f"http://10.0.2.2:{PORT}",
    "device":   f"http://{LOCAL_PC_IP}:{PORT}",
    "ngrok":    NGROK_URL,
}

BACKEND_URL = _URLS.get(ENVIRONMENT, _URLS["device"])

# APIs
API_PING           = f"{BACKEND_URL}/"
API_HEALTH         = f"{BACKEND_URL}/health"
API_BISECCION      = f"{BACKEND_URL}/biseccion"
API_FALSA_POSICION = f"{BACKEND_URL}/falsa_posicion"


def print_config():
    """Muestra la configuración actual en consola"""
    print("\n" + "╔" + "═"*50 + "╗")
    print(f"║  🔧 CONFIGURACIÓN ACTUAL")
    print("║" + " "*50 + "║")
    print(f"║  🌍 Ambiente    : {ENVIRONMENT.upper():33}║")
    print(f"║  🔗 URL Backend : {BACKEND_URL:33}║")
    print(f"║  ⚙️  Puerto      : {PORT:33}║")
    print("╚" + "═"*50 + "╝\n")


def get_backend_url(ip=None, puerto=None, environment=None):
    """
    Obtiene la URL del backend de forma dinámica
    
    Args:
        ip: IP del servidor (opcional)
        puerto: Puerto del servidor (opcional)
        environment: Ambiente ('device', 'ngrok', 'emulator') (opcional)
    
    Returns:
        URL del backend
    """
    if environment == "ngrok":
        return NGROK_URL
    elif ip and puerto:
        return f"http://{ip}:{puerto}"
    else:
        return BACKEND_URL
