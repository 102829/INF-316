import reflex as rx
import requests
import json
import hashlib
import os

# ─────────────────────────────────────────
#  COLORES
# ─────────────────────────────────────────
DARK_BG      = "#0d1117"
CARD_BG      = "#161b22"
BORDER       = "#30363d"
ACCENT       = "#58a6ff"
ACCENT_GREEN = "#3fb950"
ACCENT_ORG   = "#d29922"
TEXT_PRIMARY = "#e6edf3"
TEXT_MUTED   = "#8b949e"
RED_ERR      = "#f85149"

CARD_STYLE = {
    "background": CARD_BG,
    "border": f"1px solid {BORDER}",
    "border_radius": "12px",
    "padding": "28px",
    "width": "100%",
}
LABEL_STYLE = {
    "font_size": "12px",
    "font_weight": "600",
    "letter_spacing": "0.08em",
    "color": TEXT_MUTED,
    "text_transform": "uppercase",
    "margin_bottom": "4px",
}
INPUT_STYLE = {
    "background": "#0d1117",
    "border": f"1px solid {BORDER}",
    "border_radius": "8px",
    "color": TEXT_PRIMARY,
    "font_family": "'Courier New', monospace",
    "font_size": "14px",
    "padding": "8px 12px",
    "width": "100%",
    "_placeholder": {"color": TEXT_MUTED},
}
BTN_BLUE = {
    "background": "linear-gradient(135deg, #1f6feb 0%, #388bfd 100%)",
    "color": "#ffffff",
    "border_radius": "8px",
    "font_weight": "700",
    "font_size": "14px",
    "padding": "10px 22px",
    "border": "none",
    "cursor": "pointer",
    "transition": "all 0.15s ease",
    "width": "100%",
}
BTN_GREEN    = {**BTN_BLUE, "background": "linear-gradient(135deg, #238636 0%, #2ea043 100%)"}
BTN_CALC_BLUE  = {**BTN_BLUE,  "width": "auto", "padding": "10px 22px"}
BTN_CALC_GREEN = {**BTN_GREEN, "width": "auto", "padding": "10px 22px"}


# ─────────────────────────────────────────
#  ALMACENAMIENTO USUARIOS (JSON)
# ─────────────────────────────────────────
USERS_FILE = "users.json"

def _load_users() -> dict:
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def _save_users(users: dict):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ─────────────────────────────────────────
#  STATE
# ─────────────────────────────────────────
class State(rx.State):

    # ── Auth
    usuario_actual: str = ""
    auth_error:     str = ""
    auth_modo:      str = "login"
    login_user:     str = ""
    login_pass:     str = ""
    reg_user:       str = ""
    reg_pass:       str = ""
    reg_pass2:      str = ""

    # ── Parámetros
    ks:          str = "0.5"
    hf:          str = "15.0"
    delta_theta: str = "0.25"
    tiempo:      str = "120.0"
    f_min:       str = "0.01"
    f_max:       str = "100.0"
    tol:         str = "0.0001"

    # ── Resultados
    metodo_nombre:   str        = ""
    resultado_valor: str        = ""
    iteraciones:     list[dict] = []
    chart_data:      list[dict] = []   # ← datos para gráfica

    loading:    bool = False
    has_result: bool = False
    error_msg:  str  = ""

    # ── Historial
    historial: list[dict] = []

    # ─── Setters auth
    def set_login_user(self, v):  self.login_user = v
    def set_login_pass(self, v):  self.login_pass = v
    def set_reg_user(self, v):    self.reg_user   = v
    def set_reg_pass(self, v):    self.reg_pass   = v
    def set_reg_pass2(self, v):   self.reg_pass2  = v

    # ─── Setters parámetros
    def set_ks(self, v):          self.ks          = v
    def set_hf(self, v):          self.hf          = v
    def set_delta_theta(self, v): self.delta_theta  = v
    def set_tiempo(self, v):      self.tiempo       = v
    def set_f_min(self, v):       self.f_min        = v
    def set_f_max(self, v):       self.f_max        = v
    def set_tol(self, v):         self.tol          = v

    def cambiar_modo(self, modo: str):
        self.auth_modo  = modo
        self.auth_error = ""

    # ── Login
    def login(self):
        self.auth_error = ""
        users = _load_users()
        u, p  = self.login_user.strip(), self.login_pass
        if not u or not p:
            self.auth_error = "Completa usuario y contraseña."
            return
        if u not in users:
            self.auth_error = "Usuario no encontrado."
            return
        if users[u]["password"] != _hash(p):
            self.auth_error = "Contraseña incorrecta."
            return
        self.usuario_actual = u
        self.historial      = users[u].get("historial", [])
        return rx.redirect("/")

    # ── Registro
    def registrar(self):
        self.auth_error = ""
        u, p, p2 = self.reg_user.strip(), self.reg_pass, self.reg_pass2
        if not u or not p:
            self.auth_error = "Completa todos los campos."
            return
        if len(u) < 3:
            self.auth_error = "Usuario: mínimo 3 caracteres."
            return
        if len(p) < 6:
            self.auth_error = "Contraseña: mínimo 6 caracteres."
            return
        if p != p2:
            self.auth_error = "Las contraseñas no coinciden."
            return
        users = _load_users()
        if u in users:
            self.auth_error = "Ese usuario ya existe."
            return
        users[u] = {"password": _hash(p), "historial": []}
        _save_users(users)
        self.usuario_actual = u
        self.historial      = []
        return rx.redirect("/")

    # ── Logout
    def logout(self):
        self.usuario_actual  = ""
        self.has_result      = False
        self.error_msg       = ""
        self.iteraciones     = []
        self.chart_data      = []
        self.historial       = []
        return rx.redirect("/login")

    def check_auth(self):
        if not self.usuario_actual:
            return rx.redirect("/login")

    # ── Payload API
    def _payload(self):
        return {
            "Ks":          float(self.ks          or 0),
            "hf":          float(self.hf          or 0),
            "delta_theta": float(self.delta_theta or 0),
            "t":           float(self.tiempo      or 0),
            "F_min":       float(self.f_min       or 0),
            "F_max":       float(self.f_max       or 0),
            "tol":         float(self.tol         or 0.0001),
            "max_iter":    100,
        }

    def _procesar(self, endpoint: str):
        self.loading    = True
        self.error_msg  = ""
        self.has_result = False
        yield
        try:
            resp = requests.post(
                f"http://127.0.0.1:8001/{endpoint}",
                json=self._payload(), timeout=8,
            )
            data = resp.json()
            if "error" in data:
                self.error_msg = data["error"]
            else:
                self.metodo_nombre   = str(data.get("metodo", ""))
                self.resultado_valor = str(data.get("resultado", ""))
                self.iteraciones     = data.get("iteraciones", [])

                # ── Construir datos para gráfica recharts
                self.chart_data = [
                    {
                        "iter":  row["iter"],
                        "raiz":  float(row["c"]),
                        "error": float(row["error"]),
                    }
                    for row in self.iteraciones
                ]

                self.has_result = True

                # Guardar historial
                entrada = {
                    "metodo":      self.metodo_nombre,
                    "resultado":   self.resultado_valor,
                    "ks":          self.ks,
                    "hf":          self.hf,
                    "delta_theta": self.delta_theta,
                    "t":           self.tiempo,
                    "iteraciones": len(self.iteraciones),
                }
                self.historial = [entrada] + self.historial[:9]
                users = _load_users()
                if self.usuario_actual in users:
                    users[self.usuario_actual]["historial"] = self.historial
                    _save_users(users)

        except requests.exceptions.ConnectionError:
            self.error_msg = "No se puede conectar con la API. Corre 'python main.py' primero."
        except Exception as e:
            self.error_msg = str(e)
        finally:
            self.loading = False

    def calcular_biseccion(self):
        yield from self._procesar("biseccion")

    def calcular_falsa_posicion(self):
        yield from self._procesar("falsa_posicion")

    def limpiar(self):
        self.has_result      = False
        self.error_msg       = ""
        self.iteraciones     = []
        self.chart_data      = []
        self.metodo_nombre   = ""
        self.resultado_valor = ""


# ─────────────────────────────────────────
#  COMPONENTES REUTILIZABLES
# ─────────────────────────────────────────
def campo_auth(label, placeholder, setter, tipo="text"):
    return rx.vstack(
        rx.text(label, style=LABEL_STYLE),
        rx.input(placeholder=placeholder, on_change=setter, type=tipo, style=INPUT_STYLE),
        spacing="1", width="100%",
    )

def campo(label, placeholder, setter):
    return rx.vstack(
        rx.text(label, style=LABEL_STYLE),
        rx.input(placeholder=placeholder, on_change=setter, style=INPUT_STYLE),
        spacing="1", width="100%",
    )

def fila_iteracion(row: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(rx.text(row["iter"],  font_family="monospace", color=TEXT_MUTED,   font_size="13px")),
        rx.table.cell(rx.text(row["c"],     font_family="monospace", color=TEXT_PRIMARY, font_size="13px")),
        rx.table.cell(rx.text(row["error"], font_family="monospace", color=ACCENT_ORG,   font_size="13px")),
        style={"border_bottom": f"1px solid {BORDER}"},
    )

def fila_historial(row: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(rx.text(row["metodo"],    font_family="monospace", color=ACCENT,       font_size="12px")),
        rx.table.cell(rx.text(row["resultado"], font_family="monospace", color=ACCENT_GREEN, font_size="12px")),
        rx.table.cell(rx.text(row["ks"],        font_family="monospace", color=TEXT_MUTED,   font_size="12px")),
        rx.table.cell(rx.text(row["t"],         font_family="monospace", color=TEXT_MUTED,   font_size="12px")),
        rx.table.cell(rx.text(row["iteraciones"], font_family="monospace", color=ACCENT_ORG, font_size="12px")),
        style={"border_bottom": f"1px solid {BORDER}"},
    )


# ── Tabla de iteraciones detallada
def tabla_iteraciones_detalle() -> rx.Component:
    return rx.cond(
        State.has_result,
        rx.box(
            # Encabezado con badge del método
            rx.hstack(
                rx.icon("table-2", color=ACCENT, size=18),
                rx.heading("Tabla de Iteraciones", size="4", color=TEXT_PRIMARY),
                rx.badge(
                    State.metodo_nombre,
                    style={
                        "background": f"{ACCENT}22",
                        "color": ACCENT,
                        "border": f"1px solid {ACCENT}44",
                        "border_radius": "6px",
                        "padding": "2px 10px",
                        "font_size": "11px",
                        "font_weight": "700",
                        "text_transform": "uppercase",
                    },
                ),
                rx.spacer(),
                rx.text(
                    f"Total: ",
                    color=TEXT_MUTED, font_size="12px",
                ),
                rx.text(
                    State.iteraciones.length(),
                    color=ACCENT_GREEN, font_size="12px", font_weight="700",
                ),
                rx.text(" iteraciones", color=TEXT_MUTED, font_size="12px"),
                spacing="3", align="center", width="100%",
            ),
            rx.divider(border_color=BORDER, margin_y="16px"),

            # Tabla scrollable
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell(
                                rx.hstack(rx.icon("hash", size=13), rx.text("Iter"), spacing="1"),
                                style={"color": TEXT_MUTED, "font_size": "12px", "padding": "10px 16px",
                                       "background": "#0d1117", "font_weight": "700"},
                            ),
                            rx.table.column_header_cell(
                                rx.hstack(rx.icon("target", size=13), rx.text("c  (raíz aprox.)"), spacing="1"),
                                style={"color": TEXT_MUTED, "font_size": "12px", "padding": "10px 16px",
                                       "background": "#0d1117", "font_weight": "700"},
                            ),
                            rx.table.column_header_cell(
                                rx.hstack(rx.icon("trending-down", size=13), rx.text("Error absoluto"), spacing="1"),
                                style={"color": TEXT_MUTED, "font_size": "12px", "padding": "10px 16px",
                                       "background": "#0d1117", "font_weight": "700"},
                            ),
                        ),
                    ),
                    rx.table.body(rx.foreach(State.iteraciones, fila_iteracion)),
                    width="100%",
                ),
                max_height="320px",
                overflow_y="auto",
                border=f"1px solid {BORDER}",
                border_radius="8px",
                style={
                    "::-webkit-scrollbar": {"width": "6px"},
                    "::-webkit-scrollbar-track": {"background": CARD_BG},
                    "::-webkit-scrollbar-thumb": {"background": BORDER, "border_radius": "3px"},
                },
            ),
            style=CARD_STYLE,
        ),
        rx.fragment(),
    )


# ── Gráfica de convergencia (doble: raíz + error)
def grafica_convergencia() -> rx.Component:
    return rx.cond(
        State.has_result,
        rx.box(
            rx.hstack(
                rx.icon("chart-line", color=ACCENT_GREEN, size=18),
                rx.heading("Gráfica de Convergencia", size="4", color=TEXT_PRIMARY),
                spacing="3", align="center",
            ),
            rx.divider(border_color=BORDER, margin_y="16px"),

            # Gráfica 1: Evolución de la raíz c
            rx.text("Evolución de la raíz aproximada (c)", color=TEXT_MUTED,
                    font_size="12px", font_weight="600", margin_bottom="8px"),
            rx.recharts.line_chart(
                rx.recharts.line(
                    data_key="raiz",
                    stroke=ACCENT,
                    stroke_width=2,
                    dot={"fill": ACCENT, "r": 3},
                    name="Raíz c",
                ),
                rx.recharts.x_axis(
                    data_key="iter",
                    stroke=BORDER,
                    tick={"fill": TEXT_MUTED, "fontSize": 11},
                    label={"value": "Iteración", "position": "insideBottom",
                           "offset": -5, "fill": TEXT_MUTED, "fontSize": 11},
                ),
                rx.recharts.y_axis(
                    stroke=BORDER,
                    tick={"fill": TEXT_MUTED, "fontSize": 10},
                    width=60,
                ),
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3",
                    stroke=BORDER,
                    opacity=0.5,
                ),
                rx.recharts.graphing_tooltip(
                    content_style={
                        "background": CARD_BG,
                        "border": f"1px solid {BORDER}",
                        "border_radius": "8px",
                        "color": TEXT_PRIMARY,
                        "font_size": "12px",
                    },
                ),
                data=State.chart_data,
                width="100%",
                height=200,
                margin={"top": 10, "right": 20, "left": 0, "bottom": 20},
            ),

            rx.divider(border_color=BORDER, margin_y="20px"),

            # Gráfica 2: Error por iteración
            rx.text("Error absoluto por iteración", color=TEXT_MUTED,
                    font_size="12px", font_weight="600", margin_bottom="8px"),
            rx.recharts.line_chart(
                rx.recharts.line(
                    data_key="error",
                    stroke=ACCENT_ORG,
                    stroke_width=2,
                    dot={"fill": ACCENT_ORG, "r": 3},
                    name="Error",
                ),
                rx.recharts.x_axis(
                    data_key="iter",
                    stroke=BORDER,
                    tick={"fill": TEXT_MUTED, "fontSize": 11},
                    label={"value": "Iteración", "position": "insideBottom",
                           "offset": -5, "fill": TEXT_MUTED, "fontSize": 11},
                ),
                rx.recharts.y_axis(
                    stroke=BORDER,
                    tick={"fill": TEXT_MUTED, "fontSize": 10},
                    width=70,
                ),
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3",
                    stroke=BORDER,
                    opacity=0.5,
                ),
                rx.recharts.graphing_tooltip(
                    content_style={
                        "background": CARD_BG,
                        "border": f"1px solid {BORDER}",
                        "border_radius": "8px",
                        "color": TEXT_PRIMARY,
                        "font_size": "12px",
                    },
                ),
                data=State.chart_data,
                width="100%",
                height=200,
                margin={"top": 10, "right": 20, "left": 0, "bottom": 20},
            ),

            style=CARD_STYLE,
        ),
        rx.fragment(),
    )


def panel_resultado():
    return rx.cond(
        State.has_result,
        rx.vstack(
            rx.hstack(
                rx.icon("circle-check-big", color=ACCENT_GREEN, size=20),
                rx.heading("Infiltración Acumulada", size="4", color=TEXT_PRIMARY),
                spacing="3", align="center",
            ),
            rx.box(
                rx.text(
                    State.resultado_valor,
                    font_family="'Courier New', monospace",
                    font_size="52px", font_weight="900", color=ACCENT_GREEN,
                ),
                rx.text("cm", font_size="18px", color=TEXT_MUTED),
                text_align="center", padding="16px 0",
            ),
            style=CARD_STYLE, spacing="4",
        ),
        rx.fragment(),
    )


def panel_error():
    return rx.cond(
        State.error_msg != "",
        rx.hstack(
            rx.icon("triangle-alert", color=RED_ERR, size=18),
            rx.text(State.error_msg, color=RED_ERR, font_size="14px"),
            style={
                "background": f"{RED_ERR}15",
                "border": f"1px solid {RED_ERR}44",
                "border_radius": "8px",
                "padding": "12px 16px",
                "width": "100%",
            },
        ),
        rx.fragment(),
    )


def navbar():
    return rx.hstack(
        rx.hstack(
            rx.icon("droplets", color=ACCENT, size=22),
            rx.text("Green-Ampt", color=TEXT_PRIMARY, font_weight="800", font_size="16px"),
            spacing="2", align="center",
        ),
        rx.hstack(
            rx.icon("user", color=TEXT_MUTED, size=16),
            rx.text(State.usuario_actual, color=TEXT_MUTED, font_size="13px"),
            rx.button(
                rx.hstack(rx.icon("log-out", size=14), rx.text("Salir"), spacing="1"),
                on_click=State.logout,
                variant="ghost",
                color=RED_ERR,
                font_size="12px",
                cursor="pointer",
            ),
            spacing="3", align="center",
        ),
        justify="between", align="center", width="100%",
        padding="14px 24px",
        background=CARD_BG,
        border_bottom=f"1px solid {BORDER}",
        position="sticky", top="0", z_index="100",
    )


# ─────────────────────────────────────────
#  PÁGINA LOGIN
# ─────────────────────────────────────────
def login_page() -> rx.Component:
    return rx.box(
        rx.center(
            rx.vstack(
                rx.vstack(
                    rx.hstack(
                        rx.icon("droplets", color=ACCENT, size=32),
                        rx.heading("Green-Ampt", size="7", color=TEXT_PRIMARY, font_weight="900"),
                        spacing="3", align="center",
                    ),
                    rx.text("Métodos Numéricos · Bisección & Falsa Posición",
                            color=TEXT_MUTED, font_size="13px", text_align="center"),
                    spacing="1", align="center", margin_bottom="32px",
                ),
                rx.box(
                    # Tabs
                    rx.hstack(
                        rx.button(
                            "Iniciar sesión",
                            on_click=lambda: State.cambiar_modo("login"),
                            variant="ghost",
                            color=rx.cond(State.auth_modo == "login", ACCENT, TEXT_MUTED),
                            font_weight=rx.cond(State.auth_modo == "login", "700", "400"),
                            border_bottom=rx.cond(State.auth_modo == "login", f"2px solid {ACCENT}", "2px solid transparent"),
                            border_radius="0", font_size="14px", padding_bottom="12px",
                        ),
                        rx.button(
                            "Registrarse",
                            on_click=lambda: State.cambiar_modo("registro"),
                            variant="ghost",
                            color=rx.cond(State.auth_modo == "registro", ACCENT, TEXT_MUTED),
                            font_weight=rx.cond(State.auth_modo == "registro", "700", "400"),
                            border_bottom=rx.cond(State.auth_modo == "registro", f"2px solid {ACCENT}", "2px solid transparent"),
                            border_radius="0", font_size="14px", padding_bottom="12px",
                        ),
                        spacing="0", width="100%",
                        border_bottom=f"1px solid {BORDER}",
                        margin_bottom="24px",
                    ),
                    # Error
                    rx.cond(
                        State.auth_error != "",
                        rx.hstack(
                            rx.icon("triangle-alert", color=RED_ERR, size=16),
                            rx.text(State.auth_error, color=RED_ERR, font_size="13px"),
                            style={
                                "background": f"{RED_ERR}15",
                                "border": f"1px solid {RED_ERR}44",
                                "border_radius": "8px",
                                "padding": "10px 14px",
                                "width": "100%",
                                "margin_bottom": "16px",
                            },
                        ),
                        rx.fragment(),
                    ),
                    # Forms
                    rx.cond(
                        State.auth_modo == "login",
                        rx.vstack(
                            campo_auth("Usuario", "Tu nombre de usuario", State.set_login_user),
                            campo_auth("Contraseña", "Tu contraseña", State.set_login_pass, "password"),
                            rx.button(
                                rx.hstack(rx.icon("log-in", size=16), rx.text("Iniciar sesión"), spacing="2"),
                                on_click=State.login, style=BTN_BLUE, margin_top="8px",
                            ),
                            spacing="4", width="100%",
                        ),
                        rx.vstack(
                            campo_auth("Nombre de usuario", "Mínimo 3 caracteres",  State.set_reg_user),
                            campo_auth("Contraseña",        "Mínimo 6 caracteres",  State.set_reg_pass,  "password"),
                            campo_auth("Confirmar contraseña", "Repite la contraseña", State.set_reg_pass2, "password"),
                            rx.button(
                                rx.hstack(rx.icon("user-plus", size=16), rx.text("Crear cuenta"), spacing="2"),
                                on_click=State.registrar, style=BTN_GREEN, margin_top="8px",
                            ),
                            spacing="4", width="100%",
                        ),
                    ),
                    style={**CARD_STYLE, "width": "380px"},
                ),
                spacing="0", align="center",
            ),
            min_height="100vh",
        ),
        background=DARK_BG,
        font_family="'Segoe UI', system-ui, sans-serif",
    )


# ─────────────────────────────────────────
#  PÁGINA PRINCIPAL (PROTEGIDA)
# ─────────────────────────────────────────
def index() -> rx.Component:
    return rx.cond(
        State.usuario_actual == "",
        rx.box(
            rx.center(
                rx.vstack(
                    rx.spinner(size="3", color=ACCENT),
                    rx.text("Redirigiendo…", color=TEXT_MUTED, font_size="13px"),
                    spacing="3", align="center",
                ),
                min_height="100vh",
            ),
            background=DARK_BG,
            on_mount=State.check_auth,
        ),
        rx.box(
            navbar(),
            rx.box(
                # ─── FILA SUPERIOR: Parámetros + Resultado
                rx.flex(
                    # Panel izquierdo — parámetros
                    rx.vstack(
                        rx.box(
                            rx.text("Parámetros del suelo", style=LABEL_STYLE, margin_bottom="16px"),
                            rx.vstack(
                                campo("Conductividad hidráulica (Ks)",  "ej: 0.5 cm/h", State.set_ks),
                                campo("Altura de succión capilar (hf)", "ej: 15.0 cm",  State.set_hf),
                                campo("Diferencia de humedad (Δθ)",     "ej: 0.25",     State.set_delta_theta),
                                spacing="4",
                            ),
                            style=CARD_STYLE, margin_bottom="16px",
                        ),
                        rx.box(
                            rx.text("Parámetros de simulación", style=LABEL_STYLE, margin_bottom="16px"),
                            rx.vstack(
                                campo("Tiempo (t)", "ej: 120.0 min", State.set_tiempo),
                                rx.hstack(
                                    campo("F_min", "ej: 0.01",  State.set_f_min),
                                    campo("F_max", "ej: 100.0", State.set_f_max),
                                    spacing="3", width="100%",
                                ),
                                campo("Tolerancia", "ej: 0.0001", State.set_tol),
                                spacing="4",
                            ),
                            style=CARD_STYLE,
                        ),
                        rx.hstack(
                            rx.button(
                                rx.cond(
                                    State.loading,
                                    rx.hstack(rx.spinner(size="2"), rx.text("…"), spacing="1"),
                                    rx.hstack(rx.icon("activity", size=15), rx.text("Bisección"), spacing="2"),
                                ),
                                on_click=State.calcular_biseccion,
                                style=BTN_CALC_BLUE, disabled=State.loading,
                            ),
                            rx.button(
                                rx.cond(
                                    State.loading,
                                    rx.hstack(rx.spinner(size="2"), rx.text("…"), spacing="1"),
                                    rx.hstack(rx.icon("git-branch", size=15), rx.text("Falsa Posición"), spacing="2"),
                                ),
                                on_click=State.calcular_falsa_posicion,
                                style=BTN_CALC_GREEN, disabled=State.loading,
                            ),
                            rx.button(
                                rx.icon("rotate-ccw", size=14),
                                on_click=State.limpiar,
                                variant="ghost", color=TEXT_MUTED, title="Limpiar",
                            ),
                            spacing="2", margin_top="12px", flex_wrap="wrap",
                        ),
                        width="360px", flex_shrink="0",
                    ),

                    # Panel derecho — resultado + placeholder
                    rx.vstack(
                        panel_error(),
                        panel_resultado(),
                        rx.cond(
                            ~State.has_result & (State.error_msg == ""),
                            rx.box(
                                rx.vstack(
                                    rx.icon("flask-conical", color=BORDER, size=44),
                                    rx.text("Los resultados aparecerán aquí",           color=TEXT_MUTED,        font_size="14px"),
                                    rx.text("Ingresa parámetros y elige un método",     color=f"{TEXT_MUTED}88", font_size="12px"),
                                    spacing="2", align="center",
                                ),
                                style={
                                    **CARD_STYLE,
                                    "display": "flex",
                                    "align_items": "center",
                                    "justify_content": "center",
                                    "min_height": "220px",
                                },
                            ),
                            rx.fragment(),
                        ),
                        flex="1", spacing="4", min_width="0",
                    ),

                    spacing="6", align="start", flex_wrap="wrap",
                ),

                # ─── SECCIÓN INFERIOR: Tabla + Gráfica (ancho completo)
                rx.cond(
                    State.has_result,
                    rx.vstack(
                        rx.divider(border_color=BORDER, margin_y="24px"),

                        # Fila: Tabla | Gráfica
                        rx.flex(
                            # ── Tabla detallada
                            rx.box(tabla_iteraciones_detalle(), flex="1", min_width="320px"),

                            # ── Gráficas
                            rx.box(grafica_convergencia(), flex="1", min_width="320px"),

                            spacing="6", align="start", flex_wrap="wrap", width="100%",
                        ),

                        # ── Historial
                        rx.cond(
                            State.historial.length() > 0,
                            rx.box(
                                rx.hstack(
                                    rx.icon("history", color=TEXT_MUTED, size=18),
                                    rx.heading("Historial de cálculos", size="4", color=TEXT_PRIMARY),
                                    spacing="3", align="center",
                                ),
                                rx.divider(border_color=BORDER, margin_y="14px"),
                                rx.table.root(
                                    rx.table.header(
                                        rx.table.row(
                                            rx.table.column_header_cell("Método",   style={"color": TEXT_MUTED, "font_size": "11px"}),
                                            rx.table.column_header_cell("F (cm)",   style={"color": TEXT_MUTED, "font_size": "11px"}),
                                            rx.table.column_header_cell("Ks",       style={"color": TEXT_MUTED, "font_size": "11px"}),
                                            rx.table.column_header_cell("t",        style={"color": TEXT_MUTED, "font_size": "11px"}),
                                            rx.table.column_header_cell("Iters",    style={"color": TEXT_MUTED, "font_size": "11px"}),
                                            style={"background": "#0d1117"},
                                        ),
                                    ),
                                    rx.table.body(rx.foreach(State.historial, fila_historial)),
                                    width="100%",
                                    style={"border": f"1px solid {BORDER}", "border_radius": "8px", "overflow": "hidden"},
                                ),
                                style=CARD_STYLE,
                            ),
                            rx.fragment(),
                        ),

                        spacing="4", width="100%",
                    ),
                    rx.fragment(),
                ),

                max_width="1200px",
                margin="0 auto",
                padding="32px 24px",
            ),
            background=DARK_BG,
            min_height="100vh",
            font_family="'Segoe UI', system-ui, sans-serif",
        ),
    )


# ─────────────────────────────────────────
#  APP
# ─────────────────────────────────────────
app = rx.App(style={"background": DARK_BG, "color": TEXT_PRIMARY})
app.add_page(index, title="Green-Ampt | Métodos Numéricos", on_load=State.check_auth)
app.add_page(login_page, route="/login", title="Login · Green-Ampt")
