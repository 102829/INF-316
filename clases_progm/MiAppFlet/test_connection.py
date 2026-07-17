"""
test_connection.py - Verifica la conectividad del servidor
════════════════════════════════════════════════════════════════════════

Uso: python test_connection.py

Este script prueba:
1. Conexión local (127.0.0.1)
2. Conexión a IP local (192.168.x.x)
3. Endpoints disponibles
4. Latencia del servidor
"""

import httpx
import time
import sys
from config import LOCAL_PC_IP, NGROK_URL, PORT

def test_url(url, nombre):
    """Prueba una URL y reporta el resultado"""
    try:
        inicio = time.time()
        response = httpx.get(url, timeout=5.0)
        latencia = (time.time() - inicio) * 1000
        
        if response.status_code == 200:
            print(f"✅ {nombre:40} OK ({latencia:.1f}ms)")
            return True
        else:
            print(f"⚠️  {nombre:40} {response.status_code}")
            return False
    except httpx.ConnectError:
        print(f"❌ {nombre:40} No conecta")
        return False
    except httpx.TimeoutException:
        print(f"⏱️  {nombre:40} Timeout (>5s)")
        return False
    except Exception as e:
        print(f"❌ {nombre:40} Error: {str(e)[:20]}")
        return False

def main():
    print("\n" + "╔" + "═"*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  🔍 TEST DE CONECTIVIDAD - Green-Ampt Pro v2.0".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "═"*68 + "╝\n")

    # URLs a probar
    urls = {
        "Localhost (Misma máquina)": f"http://127.0.0.1:{PORT}/",
        "Local Network": f"http://{LOCAL_PC_IP}:{PORT}/",
        "Health Check (Local)": f"http://127.0.0.1:{PORT}/health",
        "Health Check (Red)": f"http://{LOCAL_PC_IP}:{PORT}/health",
        "Documentación Swagger": f"http://127.0.0.1:{PORT}/docs",
        "ReDoc": f"http://127.0.0.1:{PORT}/redoc",
        "Ngrok (si está configurado)": f"{NGROK_URL}/",
    }

    print("Probando conexiones...\n")
    
    resultados = {}
    for nombre, url in urls.items():
        resultados[nombre] = test_url(url, nombre)
        time.sleep(0.5)  # Pequeño delay entre pruebas

    print("\n" + "─"*68)
    print("\n📊 RESUMEN:\n")
    
    ok_count = sum(1 for v in resultados.values() if v)
    total_count = len(resultados)
    
    for nombre, resultado in resultados.items():
        icono = "✅" if resultado else "❌"
        print(f"  {icono} {nombre}")
    
    print(f"\n  {ok_count}/{total_count} pruebas exitosas")
    
    print("\n" + "─"*68)
    
    # Recomendaciones
    if ok_count == 0:
        print("\n⚠️  PROBLEMA CRÍTICO:")
        print("   El servidor no está respondiendo")
        print("   • ¿Está corriendo? → python main.py")
        print("   • ¿Puerto ocupado? → Intenta otro puerto")
        print("   • ¿Firewall bloqueando? → Desactívalo/permite 8001\n")
    elif ok_count < total_count / 2:
        print("\n⚠️  PROBLEMAS DETECTADOS:")
        if not resultados.get("Localhost (Misma máquina)"):
            print("   • Localhost no funciona → Backend no está corriendo")
        if not resultados.get("Local Network"):
            print("   • Red local no funciona → IP incorrecta o firewall")
        if not resultados.get("Ngrok (si está configurado)"):
            print("   • Ngrok no funciona → Inicia ngrok: ngrok http 8001\n")
    else:
        print("\n✅ ¡TODO OK!")
        print("   El servidor está funcionando correctamente")
        print(f"   Usa esta IP en tu app: {LOCAL_PC_IP}:{PORT}\n")
    
    print("─"*68)
    
    # Instrucciones
    print("\n📝 PRÓXIMOS PASOS:\n")
    print("  1. Si algo falló, revisa los logs en: python main.py")
    print("  2. Para ver la documentación: http://127.0.0.1:8001/docs")
    print("  3. Inicia la app: python green_ampt_flet.py")
    print(f"  4. En la app usa IP: {LOCAL_PC_IP}, Puerto: {PORT}\n")
    
    # Return code
    return 0 if ok_count > 0 else 1

if __name__ == "__main__":
    sys.exit(main())
