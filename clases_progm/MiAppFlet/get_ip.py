"""
get_ip.py - Script Helper para obtener IP Local
════════════════════════════════════════════════════════════════════════

Uso: python get_ip.py

Este script:
1. Obtiene tu IP local automáticamente
2. Muestra instrucciones para ejecutar el backend
3. Genera un código QR para conectar desde el celular
"""

import socket
import platform
import subprocess
import sys

def obtener_ip_local():
    """Obtiene la IP local de forma inteligente"""
    try:
        # Método 1: Conectar a Google DNS para obtener la IP local real
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        try:
            # Método 2: Usar socket.gethostbyname
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except:
            return "127.0.0.1"

def obtener_interfaces_red():
    """Obtiene todas las interfaces de red"""
    interfaces = []
    
    try:
        if platform.system() == "Windows":
            # Windows
            resultado = subprocess.run(
                ["ipconfig"],
                capture_output=True,
                text=True
            )
            lineas = resultado.stdout.split('\n')
            
            for linea in lineas:
                if "IPv4 Address" in linea:
                    ip = linea.split(":")[-1].strip()
                    if ip:
                        interfaces.append(ip)
        else:
            # Mac/Linux
            resultado = subprocess.run(
                ["hostname", "-I"],
                capture_output=True,
                text=True
            )
            ips = resultado.stdout.strip().split()
            interfaces.extend(ips)
    
    except:
        pass
    
    return interfaces

def mostrar_info():
    """Muestra la información de configuración"""
    
    ip_local = obtener_ip_local()
    interfaces = obtener_interfaces_red()
    puerto = 8001
    
    print("\n" + "╔" + "═"*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  🌍 CONFIGURACIÓN DE RED - Green-Ampt Pro v2.0".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╠" + "═"*68 + "╣")
    
    print("║" + " "*68 + "║")
    print(f"║  🎯 IP Local Detectada    : {ip_local:48}║")
    print(f"║  ⚙️  Puerto               : {puerto:48}║")
    print(f"║  🔗 URL Local             : http://{ip_local}:{puerto:39}║")
    
    print("║" + " "*68 + "║")
    print("╠" + "═"*68 + "╣")
    print("║" + " "*68 + "║")
    
    if interfaces:
        print("║  📡 Interfaces de Red Disponibles:                              ║")
        for i, iface in enumerate(interfaces, 1):
            print(f"║     {i}. {iface:62}║")
        print("║" + " "*68 + "║")
    
    print("╠" + "═"*68 + "╣")
    print("║" + " "*68 + "║")
    print("║  📝 PRÓXIMOS PASOS:                                             ║")
    print("║" + " "*68 + "║")
    
    print("║  1️⃣  Edita config.py y reemplaza:                              ║")
    print(f"║     LOCAL_PC_IP = \"{ip_local}\"                {' '*(40-len(ip_local))}║")
    print("║" + " "*68 + "║")
    
    print("║  2️⃣  Inicia el Backend en una Terminal:                        ║")
    print("║     python main.py                                              ║")
    print("║" + " "*68 + "║")
    
    print("║  3️⃣  Inicia el Frontend en otra Terminal:                      ║")
    print("║     python green_ampt_flet.py                                   ║")
    print("║" + " "*68 + "║")
    
    print("║  4️⃣  En la app:                                                ║")
    print(f"║     • IP Servidor: {ip_local:46}║")
    print(f"║     • Puerto: {puerto:57}║")
    print("║     • Presiona: 🔗 Conectar                                     ║")
    print("║" + " "*68 + "║")
    
    print("╠" + "═"*68 + "╣")
    print("║" + " "*68 + "║")
    print("║  ⚠️  IMPORTANTE:                                                ║")
    print("║" + " "*68 + "║")
    print("║  🔓 WIFI LOCAL: PC y Celular en la misma WiFi                  ║")
    print(f"║     Usa esta IP: {ip_local:50}║")
    print("║" + " "*68 + "║")
    print("║  📡 WIFI DIFERENTE / DATOS MÓVILES: Usa Ngrok                  ║")
    print("║     1. Descarga: https://ngrok.com/download                    ║")
    print("║     2. Ejecuta: ngrok http 8001                                ║")
    print("║     3. Copia la URL: https://xxxx-xxxx.ngrok-free.app         ║")
    print("║     4. En la app presiona: 📡 Usar Ngrok (Datos)              ║")
    print("║" + " "*68 + "║")
    print("╚" + "═"*68 + "╝\n")

def crear_archivo_config_backup(ip_local):
    """Sugiere actualizar config.py"""
    config_content = f'''# config.py - Actualizado automáticamente

ENVIRONMENT = "device"
LOCAL_PC_IP = "{ip_local}"
NGROK_URL = "https://xxxx-xxxx-xxxx.ngrok-free.app"  # Ingresa tu Ngrok URL
PORT = 8001
'''
    
    print("\n" + "─"*70)
    print("💾 Para actualizar config.py automáticamente, copia esto:")
    print("─"*70)
    print(config_content)
    print("─"*70 + "\n")

if __name__ == "__main__":
    print("\n🚀 Iniciando obtención de IP local...\n")
    
    mostrar_info()
    
    ip = obtener_ip_local()
    crear_archivo_config_backup(ip)
    
    print("\n✅ Hecho! Ahora:")
    print("   1. Actualiza config.py con tu IP")
    print("   2. Ejecuta: python main.py")
    print("   3. En otra terminal: python green_ampt_flet.py")
    print("   4. Ingresa en la app: IP={}, Puerto=8001\n".format(ip))
