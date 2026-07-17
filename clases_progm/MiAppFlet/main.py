"""""
Green-Ampt API Backend v2.0
════════════════════════════════════════════════════════════════════════

✅ Funciona en:
   • WiFi Local (misma red)
   • WiFi Diferente (con cambio manual de IP)
   • Datos Móviles (con Ngrok)

⚠️  IMPORTANTE: 
   - host='0.0.0.0' permite conexiones desde cualquier dispositivo en la red
   - CORS habilitado para todas las fuentes
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math
import uvicorn
import logging
import socket

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ════════════════════════════════════════════════════════════════════════
#  CREAR APLICACIÓN FASTAPI
# ════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="Green-Ampt API",
    description="Métodos Numéricos: Bisección y Falsa Posición para Green-Ampt",
    version="2.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ════════════════════════════════════════════════════════════════════════
#  CONFIGURAR CORS (Crítico para conexiones desde celular)
# ════════════════════════════════════════════════════════════════════════

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # ✅ Permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],              # ✅ GET, POST, DELETE, etc.
    allow_headers=["*"],              # ✅ Cualquier header
    expose_headers=["*"],
)

# ════════════════════════════════════════════════════════════════════════
#  MODELOS DE DATOS
# ════════════════════════════════════════════════════════════════════════

class Parametros(BaseModel):
    """Modelo de datos para los cálculos numéricos"""
    Ks:          float       # Conductividad hidráulica (cm/h)
    hf:          float       # Succión capilar (cm)
    delta_theta: float       # Diferencia de humedad volumétrica
    t:           float       # Tiempo (minutos)
    F_min:       float       # Límite inferior de F (cm)
    F_max:       float       # Límite superior de F (cm)
    tol:         float       # Tolerancia del error
    max_iter:    int = 100   # Máximo de iteraciones


# ════════════════════════════════════════════════════════════════════════
#  FUNCIONES DE CÁLCULO
# ════════════════════════════════════════════════════════════════════════

def ecuacion_green_ampt(F, Ks, hf, delta_theta, t):
    """
    Ecuación característica de Green-Ampt
    
    g(F) = F - Ks·t - hf·Δθ·ln(1 + F/(hf·Δθ))
    
    Args:
        F: Acumulación de infiltración (cm)
        Ks: Conductividad hidráulica
        hf: Succión capilar
        delta_theta: Diferencia de humedad
        t: Tiempo (horas)
    
    Returns:
        float: Valor de la función
    """
    try:
        if hf * delta_theta <= 0:
            return float('inf')
        if F <= -hf * delta_theta:
            return float('inf')
        
        valor = F - Ks * t - hf * delta_theta * math.log(1 + F / (hf * delta_theta))
        return valor
    
    except (ValueError, ZeroDivisionError, OverflowError):
        return float('inf')


def metodo_biseccion(params: Parametros):
    """
    Resuelve usando el método de Bisección
    
    Encuentra la raíz dividiendo el intervalo a la mitad en cada iteración
    """
    try:
        a, b = params.F_min, params.F_max
        ga = ecuacion_green_ampt(a, params.Ks, params.hf, params.delta_theta, params.t)
        gb = ecuacion_green_ampt(b, params.Ks, params.hf, params.delta_theta, params.t)

        # Verificar cambio de signo (condición para que existe raíz)
        if ga * gb >= 0:
            return {
                "error": "❌ No hay raíz en el intervalo [F_min, F_max]",
                "detalles": f"g(F_min)={ga:.4f}, g(F_max)={gb:.4f}",
                "hint": "Intenta cambiar F_min o F_max"
            }

        c_anterior = a
        iteraciones = []

        for i in range(params.max_iter):
            # Punto medio
            c = (a + b) / 2
            gc = ecuacion_green_ampt(c, params.Ks, params.hf, params.delta_theta, params.t)

            # Actualizar intervalo
            if ga * gc < 0:
                b, gb = c, gc
            else:
                a, ga = c, gc

            # Calcular error
            error = abs(b - a)
            
            iteraciones.append({
                "iter": i + 1,
                "c": round(c, 6),
                "error": round(error, 6),
                "g_c": round(gc, 6)
            })

            # Criterio de parada
            if error < params.tol:
                logger.info(f"✅ Bisección: Convergencia en iteración {i+1}")
                break

        return {
            "metodo": "Bisección",
            "resultado": round(c, 6),
            "unidad": "cm",
            "iteraciones": iteraciones,
            "num_iteraciones": len(iteraciones),
            "error_final": round(error, 6),
            "estado": "✅ Éxito"
        }
    
    except Exception as e:
        logger.error(f"Error en Bisección: {str(e)}")
        return {"error": f"Error en cálculo: {str(e)}"}


def metodo_falsa_posicion(params: Parametros):
    """
    Resuelve usando el método de Falsa Posición (Regula Falsi)
    
    Usa una línea recta entre los puntos para aproximar la raíz
    Generalmente converge más rápido que bisección
    """
    try:
        a, b = params.F_min, params.F_max
        ga = ecuacion_green_ampt(a, params.Ks, params.hf, params.delta_theta, params.t)
        gb = ecuacion_green_ampt(b, params.Ks, params.hf, params.delta_theta, params.t)

        # Verificar cambio de signo
        if ga * gb >= 0:
            return {
                "error": "❌ No hay raíz en el intervalo [F_min, F_max]",
                "detalles": f"g(F_min)={ga:.4f}, g(F_max)={gb:.4f}",
                "hint": "Intenta cambiar F_min o F_max"
            }

        c_anterior = a
        iteraciones = []

        for i in range(params.max_iter):
            # Fórmula de falsa posición
            if gb - ga == 0:
                return {"error": "❌ División por cero (pendiente = 0)"}
            
            c = b - gb * (b - a) / (gb - ga)
            gc = ecuacion_green_ampt(c, params.Ks, params.hf, params.delta_theta, params.t)

            # Actualizar intervalo
            if ga * gc < 0:
                b, gb = c, gc
            else:
                a, ga = c, gc

            # Calcular error
            error = abs(c - c_anterior)
            
            iteraciones.append({
                "iter": i + 1,
                "c": round(c, 6),
                "error": round(error, 6),
                "g_c": round(gc, 6)
            })

            # Criterio de parada
            if error < params.tol:
                logger.info(f"✅ Falsa Posición: Convergencia en iteración {i+1}")
                break
            
            c_anterior = c

        return {
            "metodo": "Falsa Posición",
            "resultado": round(c, 6),
            "unidad": "cm",
            "iteraciones": iteraciones,
            "num_iteraciones": len(iteraciones),
            "error_final": round(error, 6),
            "estado": "✅ Éxito"
        }
    
    except Exception as e:
        logger.error(f"Error en Falsa Posición: {str(e)}")
        return {"error": f"Error en cálculo: {str(e)}"}


# ════════════════════════════════════════════════════════════════════════
#  ENDPOINTS
# ════════════════════════════════════════════════════════════════════════

@app.get("/")
def inicio():
    """Endpoint de prueba - Verifica que el servidor está activo"""
    return {
        "✅ estado": "Backend Green-Ampt funcionando correctamente",
        "version": "2.0",
        "endpoints": {
            "Documentación": "/docs",
            "Health Check": "/health",
            "Bisección": "POST /biseccion",
            "Falsa Posición": "POST /falsa_posicion"
        }
    }


@app.get("/health")
def health_check():
    """
    Health Check - Verificar conexión
    Útil para comprobar si el servidor está accesible
    """
    return {
        "✅ status": "ok",
        "mensaje": "Servidor Green-Ampt activo y listo",
        "version": "2.0"
    }


@app.post("/biseccion")
def calcular_biseccion(params: Parametros):
    """
    Calcula la raíz usando el Método de Bisección
    
    📥 Parámetros esperados:
    - Ks: Conductividad hidráulica (cm/h)
    - hf: Succión capilar (cm)
    - delta_theta: Diferencia de humedad volumétrica
    - t: Tiempo (minutos)
    - F_min: Límite inferior
    - F_max: Límite superior
    - tol: Tolerancia
    - max_iter: Máximo de iteraciones
    
    📤 Retorna:
    - resultado: Valor de F en cm
    - iteraciones: Lista con detalles de cada iteración
    - num_iteraciones: Cantidad de iteraciones realizadas
    """
    logger.info(f"📊 Bisección solicitada: Ks={params.Ks}, hf={params.hf}, t={params.t}")
    resultado = metodo_biseccion(params)
    return resultado


@app.post("/falsa_posicion")
def calcular_falsa_posicion(params: Parametros):
    """
    Calcula la raíz usando el Método de Falsa Posición (Regula Falsi)
    
    📥 Parámetros esperados:
    - Ks: Conductividad hidráulica (cm/h)
    - hf: Succión capilar (cm)
    - delta_theta: Diferencia de humedad volumétrica
    - t: Tiempo (minutos)
    - F_min: Límite inferior
    - F_max: Límite superior
    - tol: Tolerancia
    - max_iter: Máximo de iteraciones
    
    📤 Retorna:
    - resultado: Valor de F en cm
    - iteraciones: Lista con detalles de cada iteración
    - num_iteraciones: Cantidad de iteraciones realizadas
    """
    logger.info(f"📊 Falsa Posición solicitada: Ks={params.Ks}, hf={params.hf}, t={params.t}")
    resultado = metodo_falsa_posicion(params)
    return resultado


# ════════════════════════════════════════════════════════════════════════
#  OBTENER IP LOCAL
# ════════════════════════════════════════════════════════════════════════

def obtener_ip_local():
    """Obtiene la IP local del servidor"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


# ════════════════════════════════════════════════════════════════════════
#  MAIN - INICIAR SERVIDOR
# ════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    
    ip_local = obtener_ip_local()
    
    print("\n" + "╔" + "═"*70 + "╗")
    print("║" + " "*70 + "║")
    print("║" + "  🚀 INICIANDO SERVIDOR GREEN-AMPT API v2.0".center(70) + "║")
    print("║" + " "*70 + "║")
    print("╠" + "═"*70 + "╣")
    print("║" + " "*70 + "║")
    print(f"║  📍 IP Local         : {ip_local:50} ║")
    print(f"║  🔗 URL Local        : http://{ip_local}:8001:46 ║")
    print("║  🌐 URL Docs         : http://127.0.0.1:8001/docs                   ║")
    print("║  💊 Health Check     : http://127.0.0.1:8001/health                 ║")
    print("║" + " "*70 + "║")
    print("╠" + "═"*70 + "╣")
    print("║  ⚠️  IMPORTANTE:                                                      ║")
    print("║" + " "*70 + "║")
    print("║  ✅ host='0.0.0.0' permite conexiones desde:                         ║")
    print("║     • Dispositivos en la misma WiFi                                   ║")
    print("║     • Dispositivos en WiFi diferente (cambiando IP)                  ║")
    print("║     • Datos móviles (con Ngrok)                                      ║")
    print("║" + " "*70 + "║")
    print("║  📱 Para conectar desde celular:                                     ║")
    print(f"║     1. Usa la IP local: {ip_local}:8001                           ║")
    print("║     2. O cambia la IP desde la app si estás en otra red             ║")
    print("║     3. O usa Ngrok para datos móviles                                ║")
    print("║" + " "*70 + "║")
    print("╚" + "═"*70 + "╝\n")
    
    # ⚠️ CRÍTICO: host DEBE ser 0.0.0.0
    uvicorn.run(
        "main:app",
        host="0.0.0.0",      # 🔴 OBLIGATORIO - Escucha en TODAS las interfaces
        port=8001,
        reload=True,
        log_level="info"
    )
