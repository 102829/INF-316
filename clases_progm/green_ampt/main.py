from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math

app = FastAPI(
    title="API Green-Ampt",
    description="Métodos numéricos: Bisección y Falsa Posición",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Datos(BaseModel):
    Ks: float
    hf: float
    delta_theta: float
    t: float
    F_min: float
    F_max: float
    tol: float
    max_iter: int = 100


def g(F, Ks, hf, delta_theta, t):
    try:
        return F - Ks*t - hf*delta_theta*math.log(1 + F/(hf*delta_theta))
    except:
        return float('inf')


def biseccion(data: Datos):
    a, b = data.F_min, data.F_max
    ga = g(a, data.Ks, data.hf, data.delta_theta, data.t)
    gb = g(b, data.Ks, data.hf, data.delta_theta, data.t)

    if ga * gb >= 0:
        return {"error": "No hay raíz en el intervalo dado"}

    c_anterior = a
    iteraciones = []

    for i in range(data.max_iter):
        c = (a + b) / 2
        gc = g(c, data.Ks, data.hf, data.delta_theta, data.t)

        if ga * gc < 0:
            b, gb = c, gc
        else:
            a, ga = c, gc

        error = abs(c - c_anterior)
        iteraciones.append({"iter": i + 1, "c": round(c, 6), "error": round(error, 6)})

        if error < data.tol:
            break
        c_anterior = c

    return {"metodo": "biseccion", "resultado": round(c, 6), "iteraciones": iteraciones}


def falsa_posicion(data: Datos):
    a, b = data.F_min, data.F_max
    ga = g(a, data.Ks, data.hf, data.delta_theta, data.t)
    gb = g(b, data.Ks, data.hf, data.delta_theta, data.t)

    if ga * gb >= 0:
        return {"error": "No hay raíz en el intervalo dado"}

    c_anterior = a
    iteraciones = []

    for i in range(data.max_iter):
        c = b - gb * (b - a) / (gb - ga)
        gc = g(c, data.Ks, data.hf, data.delta_theta, data.t)

        if ga * gc < 0:
            b, gb = c, gc
        else:
            a, ga = c, gc

        error = abs(c - c_anterior)
        iteraciones.append({"iter": i + 1, "c": round(c, 6), "error": round(error, 6)})

        if error < data.tol:
            break
        c_anterior = c

    return {"metodo": "falsa_posicion", "resultado": round(c, 6), "iteraciones": iteraciones}


@app.get("/")
def inicio():
    return {"mensaje": "API Green-Ampt funcionando 🚀"}

@app.post("/biseccion")
def resolver_biseccion(data: Datos):
    return biseccion(data)

@app.post("/falsa_posicion")
def resolver_falsa_posicion(data: Datos):
    return falsa_posicion(data)


if __name__ == "__main__":
    import uvicorn
    print("\n🚀 API iniciada → http://127.0.0.1:8000")
    print("📄 Docs       → http://127.0.0.1:8000/docs\n")
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
