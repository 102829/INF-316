"""
Green-Ampt Pro v2.0 - VERSIÓN APK CORREGIDA
════════════════════════════════════════════════════════════════════════

✅ CAMBIOS:
   • Sin IP hardcodeada (ingresa tu IP real)
   • Mejor manejo de errores
   • Validación clara de conexión
   • Compatible con Redmi 13C

⚠️  El backend (main.py) debe estar corriendo en tu PC
"""

import flet as ft
import httpx
import json
import os
import hashlib
from datetime import datetime

# ════════════════════════════════════════════════════════════════════════
#  CONFIGURACIÓN PARA APK (sin IP hardcodeada)
# ════════════════════════════════════════════════════════════════════════

DEFAULT_IP = ""                    # ✅ VACÍO - Ingresa tu IP real
DEFAULT_PORT = 8001
DEFAULT_NGROK = "https://xxxx-xxxx-xxxx.ngrok-free.app"

# ════════════════════════════════════════════════════════════════════════
#  COLORES Y ESTILOS
# ════════════════════════════════════════════════════════════════════════

COLOR_BG = "#0f172a"          # Azul muy oscuro (fondo)
COLOR_CARD = "#1e293b"        # Azul oscuro (tarjetas)
COLOR_CARD_HOVER = "#334155"  # Azul medio
COLOR_BLUE = "#3b82f6"        # Azul
COLOR_GREEN = "#10b981"       # Verde
COLOR_RED = "#ef4444"         # Rojo
COLOR_YELLOW = "#f59e0b"      # Amarillo
COLOR_TEXT = "#f8fafc"        # Blanco
COLOR_TEXT2 = "#94a3b8"       # Gris claro

# ════════════════════════════════════════════════════════════════════════
#  GESTIÓN DE USUARIOS
# ════════════════════════════════════════════════════════════════════════

USERS_FILE = "users.json"

def cargar_usuarios():
    """Carga el archivo de usuarios"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        else:
            # Usuarios demo por defecto
            return {
                "david": {"password": hashlib.sha256("123".encode()).hexdigest(), "historial": []},
                "daniel": {"password": hashlib.sha256("1234".encode()).hexdigest(), "historial": []},
                "elisa": {"password": hashlib.sha256("1234".encode()).hexdigest(), "historial": []}
            }
    except:
        return {}

def guardar_usuarios(usuarios):
    """Guarda el archivo de usuarios"""
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(usuarios, f, indent=4)
    except:
        pass

def hash_password(password):
    """Hash seguro de contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

# ════════════════════════════════════════════════════════════════════════
#  APLICACIÓN PRINCIPAL
# ════════════════════════════════════════════════════════════════════════

def main(page: ft.Page):
    """Función principal de la aplicación"""
    
    page.title = "Green-Ampt Pro v2.0"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = COLOR_BG
    page.scroll = "auto"
    page.padding = 0
    
    try:
        page.window_width = 420
        page.window_height = 900
    except:
        # En APK no se puede cambiar el tamaño
        pass

    # Variables globales
    estado = {
        "conectado": False,
        "backend_url": f"http://{DEFAULT_IP}:{DEFAULT_PORT}" if DEFAULT_IP else "",
        "usuario": None,
        "ip": DEFAULT_IP,
        "puerto": DEFAULT_PORT,
        "modo": "device"  # device, ngrok
    }

    # ════════════════════════════════════════════════════════════════
    #  PANTALLA DE LOGIN
    # ════════════════════════════════════════════════════════════════

    def pantalla_login():
        """Pantalla de autenticación"""
        
        usuario_input = ft.TextField(
            label="👤 Usuario",
            border_color=COLOR_BLUE,
            color=COLOR_TEXT,
            focused_border_color=COLOR_GREEN,
            width=300
        )

        password_input = ft.TextField(
            label="🔐 Contraseña",
            password=True,
            can_reveal_password=True,
            border_color=COLOR_BLUE,
            color=COLOR_TEXT,
            focused_border_color=COLOR_GREEN,
            width=300
        )

        mensaje = ft.Text("", color=COLOR_RED, size=12)

        def iniciar_sesion(e):
            """Verifica credenciales y accede"""
            usuarios = cargar_usuarios()
            u = usuario_input.value.strip()
            p = hash_password(password_input.value)

            if u == "" or password_input.value == "":
                mensaje.value = "⚠️ Completa todos los campos"
                mensaje.color = COLOR_RED
            elif u in usuarios and usuarios[u]["password"] == p:
                estado["usuario"] = u
                mensaje.value = "✅ Acceso correcto"
                mensaje.color = COLOR_GREEN
                page.update()
                
                # Pequeño delay
                import time
                time.sleep(0.5)
                pantalla_principal()
            else:
                mensaje.value = "❌ Usuario o contraseña incorrectos"
                mensaje.color = COLOR_RED

            page.update()

        def registrar(e):
            """Registra un nuevo usuario"""
            usuarios = cargar_usuarios()
            u = usuario_input.value.strip()
            p = password_input.value

            if u == "" or p == "":
                mensaje.value = "⚠️ Completa todos los campos"
                mensaje.color = COLOR_RED
            elif len(p) < 4:
                mensaje.value = "⚠️ Contraseña mínimo 4 caracteres"
                mensaje.color = COLOR_RED
            elif u in usuarios:
                mensaje.value = "⚠️ El usuario ya existe"
                mensaje.color = COLOR_RED
            else:
                usuarios[u] = {"password": hash_password(p), "historial": []}
                guardar_usuarios(usuarios)
                mensaje.value = "✅ Usuario registrado"
                mensaje.color = COLOR_GREEN
                usuario_input.value = ""
                password_input.value = ""

            page.update()

        # UI de Login
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Container(height=20),
                    
                    ft.Text("💧", size=70, text_align="center"),
                    
                    ft.Text(
                        "GREEN-AMPT PRO",
                        size=28,
                        weight="bold",
                        color=COLOR_TEXT,
                        text_align="center"
                    ),
                    
                    ft.Text(
                        "Sistema de Infiltración v2.0",
                        size=12,
                        color=COLOR_TEXT2,
                        text_align="center"
                    ),
                    
                    ft.Container(height=30),
                    
                    usuario_input,
                    password_input,
                    mensaje,
                    
                    ft.Container(height=15),
                    
                    ft.FilledButton(
                        "🔓 Iniciar Sesión",
                        width=300,
                        bgcolor=COLOR_BLUE,
                        color="white",
                        on_click=iniciar_sesion
                    ),
                    
                    ft.OutlinedButton(
                        "📝 Registrarse",
                        width=300,
                        on_click=registrar
                    ),

                    ft.Container(height=20),
                    
                    ft.Text(
                        "Usuarios demo: david/123 | daniel/1234",
                        size=10,
                        color=COLOR_TEXT2,
                        text_align="center"
                    ),
                    
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=COLOR_BG,
                padding=20
            )
        )

    # ════════════════════════════════════════════════════════════════
    #  PANTALLA PRINCIPAL
    # ════════════════════════════════════════════════════════════════

    def pantalla_principal():
        """Pantalla principal de cálculos"""
        
        # ═══════════════════════════════════════════════════════════
        #  SECCIÓN 1: CONFIGURACIÓN DE CONEXIÓN
        # ═══════════════════════════════════════════════════════════

        ip_input = ft.TextField(
            label="🌐 IP del Servidor",
            value=estado["ip"],
            width=280,
            hint_text="Ej: 192.168.1.100"
        )

        puerto_input = ft.TextField(
            label="🔌 Puerto",
            value=str(estado["puerto"]),
            width=280,
            hint_text="Default: 8001"
        )

        url_display = ft.Text(
            f"URL: http://{estado['ip']}:{estado['puerto']}",
            size=11,
            color=COLOR_TEXT2
        )

        estado_conexion = ft.Text(
            "❌ No conectado",
            size=12,
            color=COLOR_RED
        )

        def conectar(e):
            """Intenta conectar al servidor"""
            try:
                ip = ip_input.value.strip()
                puerto = puerto_input.value.strip()
                
                if not ip:
                    estado_conexion.value = "❌ Ingresa la IP del servidor"
                    estado_conexion.color = COLOR_RED
                    page.update()
                    return
                
                if not puerto:
                    puerto = "8001"
                    puerto_input.value = "8001"
                
                estado["ip"] = ip
                estado["puerto"] = int(puerto)
                estado["backend_url"] = f"http://{ip}:{puerto}"
                estado["modo"] = "device"
                
                url_display.value = f"URL: {estado['backend_url']}"
                
                # Test de conexión
                estado_conexion.value = "⏳ Probando conexión..."
                estado_conexion.color = COLOR_YELLOW
                page.update()

                with httpx.Client(timeout=5.0) as client:
                    response = client.get(f"{estado['backend_url']}/health")
                    
                if response.status_code == 200:
                    estado["conectado"] = True
                    estado_conexion.value = "✅ Conectado"
                    estado_conexion.color = COLOR_GREEN
                else:
                    estado["conectado"] = False
                    estado_conexion.value = f"❌ Error HTTP {response.status_code}"
                    estado_conexion.color = COLOR_RED
                
            except httpx.ConnectError:
                estado["conectado"] = False
                estado_conexion.value = "❌ Servidor no accesible\n   Verifica IP y puerto"
                estado_conexion.color = COLOR_RED
            except httpx.TimeoutException:
                estado["conectado"] = False
                estado_conexion.value = "❌ Timeout: Servidor tardó mucho"
                estado_conexion.color = COLOR_RED
            except ValueError as ex:
                estado["conectado"] = False
                estado_conexion.value = "❌ Puerto debe ser un número"
                estado_conexion.color = COLOR_RED
            except Exception as ex:
                estado["conectado"] = False
                estado_conexion.value = f"❌ Error: {str(ex)[:30]}"
                estado_conexion.color = COLOR_RED
            
            page.update()

        btn_conectar = ft.FilledButton(
            "🔗 Conectar",
            width=280,
            bgcolor=COLOR_BLUE,
            color="white",
            on_click=conectar
        )

        # Botones para Ngrok
        def usar_ngrok(e):
            """Usa la URL de Ngrok"""
            ip_input.value = "Ngrok"
            estado["backend_url"] = DEFAULT_NGROK
            estado["modo"] = "ngrok"
            puerto_input.value = ""
            url_display.value = f"URL: {DEFAULT_NGROK}"
            page.update()
            conectar(None)

        btn_ngrok = ft.OutlinedButton(
            "📡 Usar Ngrok (Datos)",
            width=280,
            on_click=usar_ngrok
        )

        # ═══════════════════════════════════════════════════════════
        #  SECCIÓN 2: PARÁMETROS DE CÁLCULO
        # ═══════════════════════════════════════════════════════════

        ks_input = ft.TextField(label="🌾 Ks (cm/h)", value="0.5", width=130)
        hf_input = ft.TextField(label="💧 hf (cm)", value="15", width=130)
        dtheta_input = ft.TextField(label="📊 Δθ", value="0.25", width=130)
        tiempo_input = ft.TextField(label="⏱️ Tiempo (min)", value="120", width=130)
        fmin_input = ft.TextField(label="📉 F_min (cm)", value="0.01", width=130)
        fmax_input = ft.TextField(label="📈 F_max (cm)", value="100", width=130)
        tol_input = ft.TextField(label="🎯 Tolerancia", value="0.0001", width=130)

        resultado_text = ft.Text(
            "",
            size=24,
            weight="bold",
            color=COLOR_GREEN
        )

        error_text = ft.Text("", color=COLOR_RED, size=12)

        tabla_iteraciones = ft.Column(spacing=5)

        # ═══════════════════════════════════════════════════════════
        #  FUNCIONES DE CÁLCULO
        # ═══════════════════════════════════════════════════════════

        def calcular_metodo(metodo):
            """Realiza el cálculo en el servidor"""
            
            if not estado["conectado"]:
                error_text.value = "❌ Debes conectarte primero"
                error_text.color = COLOR_RED
                page.update()
                return
            
            try:
                resultado_text.value = "⏳ Calculando..."
                resultado_text.color = COLOR_YELLOW
                error_text.value = ""
                tabla_iteraciones.controls.clear()
                page.update()

                payload = {
                    "Ks": float(ks_input.value),
                    "hf": float(hf_input.value),
                    "delta_theta": float(dtheta_input.value),
                    "t": float(tiempo_input.value),
                    "F_min": float(fmin_input.value),
                    "F_max": float(fmax_input.value),
                    "tol": float(tol_input.value),
                    "max_iter": 100
                }

                url_endpoint = f"{estado['backend_url']}/{metodo}"
                
                with httpx.Client(timeout=10.0) as client:
                    response = client.post(url_endpoint, json=payload)
                    data = response.json()

                if "error" in data:
                    resultado_text.value = ""
                    error_text.value = f"❌ {data['error']}"
                    error_text.color = COLOR_RED
                else:
                    resultado = data.get("resultado", "N/A")
                    unidad = data.get("unidad", "")
                    num_iter = data.get("num_iteraciones", 0)
                    metodo_nombre = data.get("metodo", metodo)
                    
                    resultado_text.value = f"📊 {resultado} {unidad}"
                    resultado_text.color = COLOR_GREEN

                    # Mostrar algunas iteraciones
                    iteraciones = data.get("iteraciones", [])
                    for i, iter_data in enumerate(iteraciones[-5:]):  # Últimas 5
                        tabla_iteraciones.controls.append(
                            ft.Container(
                                content=ft.Row([
                                    ft.Text(f"#{iter_data['iter']}", width=40, size=10),
                                    ft.Text(f"c: {iter_data['c']}", width=100, size=10),
                                    ft.Text(f"err: {iter_data['error']:.2e}", width=120, size=10),
                                ], spacing=5),
                                bgcolor=COLOR_CARD,
                                padding=8,
                                border_radius=8
                            )
                        )

                    error_text.value = f"✅ {metodo_nombre} - {num_iter} iteraciones"
                    error_text.color = COLOR_GREEN

            except ValueError:
                resultado_text.value = ""
                error_text.value = "⚠️ Valores numéricos inválidos"
                error_text.color = COLOR_YELLOW
            except Exception as ex:
                resultado_text.value = ""
                error_text.value = f"❌ Error: {str(ex)[:50]}"
                error_text.color = COLOR_RED

            page.update()

        def cerrar_sesion(e):
            """Cierra la sesión del usuario"""
            estado["usuario"] = None
            estado["conectado"] = False
            pantalla_login()

        # ═══════════════════════════════════════════════════════════
        #  RENDER DE LA PANTALLA PRINCIPAL
        # ═══════════════════════════════════════════════════════════

        page.clean()
        page.add(
            # Header
            ft.Container(
                content=ft.Row([
                    ft.Text("💧 Green-Ampt", size=20, weight="bold"),
                    ft.TextButton(f"👤 {estado['usuario']}", on_click=cerrar_sesion)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor=COLOR_CARD,
                padding=15
            ),

            # Contenido principal
            ft.Container(
                content=ft.Column([
                    # Sección de conexión
                    ft.Text("🔧 CONEXIÓN", size=16, weight="bold", color=COLOR_TEXT),
                    
                    ip_input,
                    puerto_input,
                    url_display,
                    
                    ft.Row([btn_conectar, btn_ngrok], spacing=5),
                    
                    ft.Container(
                        content=ft.Text(
                            "⚠️ Para obtener tu IP:\n"
                            "1. En tu PC ejecuta: ipconfig (Windows) o ifconfig (Linux/Mac)\n"
                            "2. Busca 'IPv4 Address' o similar (ej: 192.168.x.x)\n"
                            "3. Ingresa esa IP en el campo arriba",
                            size=10,
                            color=COLOR_TEXT2
                        ),
                        bgcolor=COLOR_CARD,
                        padding=10,
                        border_radius=8
                    ),
                    ft.Container(height=10),
                    
                    estado_conexion,
                    
                    ft.Divider(height=20, color=COLOR_CARD_HOVER),

                    # Sección de parámetros
                    ft.Text("📋 PARÁMETROS", size=16, weight="bold", color=COLOR_TEXT),
                    
                    ft.Row([ks_input, hf_input], spacing=10),
                    ft.Row([dtheta_input, tiempo_input], spacing=10),
                    ft.Row([fmin_input, fmax_input], spacing=10),
                    tol_input,
                    
                    ft.Divider(height=20, color=COLOR_CARD_HOVER),

                    # Sección de botones de cálculo
                    ft.Row([
                        ft.FilledButton(
                            "📐 Bisección",
                            width=130,
                            bgcolor=COLOR_BLUE,
                            color="white",
                            on_click=lambda e: calcular_metodo("biseccion")
                        ),
                        ft.FilledButton(
                            "📏 Falsa Posición",
                            width=130,
                            bgcolor=COLOR_GREEN,
                            color="white",
                            on_click=lambda e: calcular_metodo("falsa_posicion")
                        )
                    ], spacing=10),

                    ft.Divider(height=20, color=COLOR_CARD_HOVER),

                    # Resultados
                    ft.Text("📊 RESULTADOS", size=16, weight="bold", color=COLOR_TEXT),
                    resultado_text,
                    error_text,
                    
                    ft.Text("📈 Iteraciones", size=12, color=COLOR_TEXT2),
                    tabla_iteraciones,

                ], spacing=8, scroll="auto"),
                bgcolor=COLOR_BG,
                padding=15
            )
        )

    # ════════════════════════════════════════════════════════════════
    #  INICIAR APLICACIÓN
    # ════════════════════════════════════════════════════════════════

    pantalla_login()


# Ejecutar la app
ft.app(target=main)
