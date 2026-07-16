from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import numpy as np

app = FastAPI(
    title="Milne FDE Solver API",
    description="API para resolver Ecuaciones Diferenciales Difusas usando el Metodo de Milne Predictor-Corrector de 4 orden. Ejemplo 5.1: y'(t) = y(t), y(0;r) = [0.75+0.25r, 1.125-0.125r]",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Modelos ──────────────────────────────────────────

class EntradaMilne(BaseModel):
    N: int = Field(default=20, ge=4, le=100, description="Numero de pasos (4 a 100)")
    r: float = Field(default=0.5, ge=0.0, le=1.0, description="Nivel de corte alfa (0.0 a 1.0)")


class PuntoResultado(BaseModel):
    t: float
    y_low_exacta: float
    y_low_milne: float
    error_inf: float
    y_up_exacta: float
    y_up_milne: float
    error_sup: float


class RespuestaMilne(BaseModel):
    N: int
    r: float
    h: float
    error_maximo: float
    puntos: list[PuntoResultado]


# ── Matematica ───────────────────────────────────────

def exact(t, r):
    yl = (0.75 + 0.25 * r) * np.exp(t)
    yu = (1.125 - 0.125 * r) * np.exp(t)
    return yl, yu


def rk4(y, h):
    k1 = y
    k2 = y + h / 2 * k1
    k3 = y + h / 2 * k2
    k4 = y + h * k3
    return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def calcular_milne(N, r):
    h = 1.0 / N
    t = np.linspace(0, 1, N + 1)
    yl = np.zeros(N + 1)
    yu = np.zeros(N + 1)
    yl[0], yu[0] = exact(0, r)
    for i in range(min(3, N)):
        yl[i + 1] = rk4(yl[i], h)
        yu[i + 1] = rk4(yu[i], h)
    if N >= 4:
        for i in range(3, N):
            pl = yl[i-3] + (4*h/3) * (2*yl[i] - yl[i-1] + 2*yl[i-2])
            pu = yu[i-3] + (4*h/3) * (2*yu[i] - yu[i-1] + 2*yu[i-2])
            yl[i+1] = yl[i-1] + (h/3) * (pl + 4*yl[i] + yl[i-1])
            yu[i+1] = yu[i-1] + (h/3) * (pu + 4*yu[i] + yu[i-1])
    return t, yl, yu


# ── Endpoints ────────────────────────────────────────

@app.get("/", tags=["Info"])
def raiz():
    return {
        "mensaje": "Milne FDE Solver API",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoint_principal": "/calcular"
    }


@app.post("/calcular", response_model=RespuestaMilne, tags=["Milne"])
def calcular(entrada: EntradaMilne):
    """
    Resuelve la ecuacion diferencial difusa usando el Metodo de Milne.

    - **N**: numero de pasos de integracion (4 a 100)
    - **r**: nivel de corte alfa del numero difuso (0.0 a 1.0)

    Retorna los valores exactos, aproximados y errores para cada punto t.
    """
    N = entrada.N
    r = entrada.r
    t, yl_m, yu_m = calcular_milne(N, r)
    yl_e, yu_e = exact(t, r)

    puntos = []
    for i in range(len(t)):
        el = abs(float(yl_e[i]) - float(yl_m[i]))
        eu = abs(float(yu_e[i]) - float(yu_m[i]))
        puntos.append(PuntoResultado(
            t=round(float(t[i]), 6),
            y_low_exacta=round(float(yl_e[i]), 8),
            y_low_milne=round(float(yl_m[i]), 8),
            error_inf=float('{:.2e}'.format(el)),
            y_up_exacta=round(float(yu_e[i]), 8),
            y_up_milne=round(float(yu_m[i]), 8),
            error_sup=float('{:.2e}'.format(eu)),
        ))

    emax = float(max(
        np.max(np.abs(yl_e - yl_m)),
        np.max(np.abs(yu_e - yu_m))
    ))

    return RespuestaMilne(
        N=N,
        r=r,
        h=round(1.0 / N, 6),
        error_maximo=float('{:.2e}'.format(emax)),
        puntos=puntos,
    )


@app.get("/salud", tags=["Info"])
def salud():
    """Verifica que la API esta funcionando correctamente."""
    return {"estado": "ok", "servicio": "Milne FDE Solver"}
