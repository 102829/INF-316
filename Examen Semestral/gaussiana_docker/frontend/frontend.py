import httpx
import asyncio
from nicegui import ui, app

# URL interna de la red de Docker
BACKEND_URL = "http://gauss_backend:8000/api/v1/elimination-gauss"

DEFAULT_A = [
    ["5", "2", "1"],
    ["1", "4", "2"],
    ["1", "2", "5"],
]
DEFAULT_B = ["11", "15", "20"]

def crear_interfaz():
    ui.add_head_html("""
    <style>
      body { background: linear-gradient(135deg, #0f0c29, #1a1040, #24243e); min-height: 100vh; }
      .card { background: rgba(15,23,42,0.95) !important; border: 1px solid rgba(139,92,246,0.3) !important; border-radius: 20px !important; }
      .titulo { font-size: 26px; font-weight: 800; color: white; }
      .subtitulo { font-size: 12px; color: #94a3b8; letter-spacing: 0.1em; text-transform: uppercase; }
      .label { font-size: 12px; font-weight: 700; color: #c4b5fd; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 8px; }
      .resultado-box { background: rgba(139,92,246,0.08); border: 1px solid rgba(139,92,246,0.25); border-radius: 12px; padding: 16px; }
      .q-field__control { background: rgba(30,20,60,0.8) !important; border-color: rgba(139,92,246,0.4) !important; }
      .q-field__native { color: #e2e8f0 !important; font-family: monospace !important; text-align: center !important; }
      .q-btn { border-radius: 10px !important; font-weight: 700 !important; }
    </style>
    """)

    with ui.column().classes("items-center justify-center w-full min-h-screen p-4"):
        with ui.card().classes("card w-full max-w-lg p-8"):

            # ── Encabezado ──
            with ui.row().classes("items-center gap-3 mb-4"):
                ui.label("📐").style("font-size:32px")
                with ui.column().classes("gap-0"):
                    ui.label("Eliminación Gaussiana").classes("titulo")
                    ui.label("Métodos Numéricos · Universidad de Panamá").classes("subtitulo")

            ui.separator().style("background:rgba(139,92,246,0.3); margin: 16px 0")

            # ── Matriz A ──
            ui.label("Matriz A (3×3)").classes("label")
            celdas_a = []
            with ui.grid(columns=3).classes("gap-2 mb-4"):
                for i in range(3):
                    fila = []
                    for j in range(3):
                        inp = ui.input(value=DEFAULT_A[i][j]).props('dense outlined').style("width:90px; border-radius:8px;")
                        inp.props('input-style="color:#e2e8f0; font-family:monospace; text-align:center"')
                        fila.append(inp)
                    celdas_a.append(fila)

            # ── Vector B ──
            ui.label("Vector B").classes("label")
            celdas_b = []
            with ui.row().classes("gap-2 mb-6"):
                for j in range(3):
                    inp = ui.input(value=DEFAULT_B[j]).props('dense outlined').style("width:90px; border-radius:8px;")
                    inp.props('input-style="color:#e2e8f0; font-family:monospace; text-align:center"')
                    celdas_b.append(inp)

            # ── Respuestas y errores ──
            error_label = ui.label("").style(
                "color:#f87171; background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); border-radius:8px; padding:10px 14px; width:100%; display:none"
            )
            resultado_box = ui.column().classes("resultado-box w-full gap-2").style("display:none")

            with resultado_box:
                ui.label("Resultado").classes("label")
                sol_label  = ui.label("").style("color:#e2e8f0; font-family:monospace; font-size:13px")
                iter_label = ui.label("").style("color:#e2e8f0; font-size:13px")
                cond_label = ui.label("").style("color:#e2e8f0; font-size:13px")
                time_label = ui.label("").style("color:#e2e8f0; font-size:13px")
                ui.badge("✅ Cálculo Exitoso", color="green").style("margin-top:4px")

            # ── Botón Resolver ──
            async def resolver():
                error_label.style("display:none")
                resultado_box.style("display:none")
                
                try:
                    A = [[float(celdas_a[i][j].value) for j in range(3)] for i in range(3)]
                    b = [float(celdas_b[j].value) for j in range(3)]
                except ValueError:
                    error_label.set_text("⚠️ Ingresa solo números válidos en todos los campos.")
                    error_label.style("display:block")
                    return

                try:
                    # Agregamos límites de reintentos y timeouts claros
                    async with httpx.AsyncClient(timeout=5.0) as client:
                        resp = await client.post(BACKEND_URL, json={"A": A, "b": b})
                    
                    if resp.status_code == 200:
                        data = resp.json()
                        sol = [round(x, 6) for x in data["vector_solucion_x"]]
                        sol_label.set_text(f"Solución X:           {sol}")
                        iter_label.set_text(f"Iteraciones:          {data['iteraciones_reales']}")
                        cond_label.set_text(f"Número de condición:  {data['numero_condicion_estimado']}")
                        time_label.set_text(f"Tiempo (ms):          {data['tiempo_ejecucion_ms']}")
                        resultado_box.style("display:flex")
                    else:
                        detalle = resp.json().get("detail", "Error interno del backend.")
                        error_label.set_text(f"⚠️ Error {resp.status_code}: {detalle}")
                        error_label.style("display:block")
                except httpx.ConnectError:
                    error_label.set_text("⚠️ Error de red: No se pudo conectar con el contenedor backend.")
                    error_label.style("display:block")
                except Exception as e:
                    error_label.set_text(f"⚠️ Error inesperado: {str(e)}")
                    error_label.style("display:block")

            ui.button("▶ Resolver", on_click=resolver).props("unelevated").style(
                "background: linear-gradient(135deg,#7c3aed,#6d28d9); color:white; font-weight:700; font-size:15px; padding:10px 32px; border-radius:10px; margin-top:8px"
            )

crear_interfaz()

# Mantener reload=False en Docker para evitar loops infinitos de recarga
ui.run(host="0.0.0.0", port=8003, title="Eliminación Gaussiana", favicon="📐", dark=True, reload=False)
