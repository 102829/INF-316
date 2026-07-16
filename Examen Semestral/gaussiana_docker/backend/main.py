from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

app = FastAPI(title="API de Métodos Numéricos")

#  datos de entrada 
class MatrixInput(BaseModel):
    A: list[list[float]]
    b: list[float]

# 2. Eliminación de Gauss
def gaussian_elimination(A: list[list[float]], b: list[float]):
    n = len(A)
    
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    iterations = 0

    
    for i in range(n):
        
        if M[i][i] == 0.0:
            raise ValueError("Matriz singular o requiere pivoteo. Cero en la diagonal.")
        
        for j in range(i + 1, n):
            factor = M[j][i] / M[i][i]
            for k in range(i, n + 1):
                M[j][k] -= factor * M[i][k]
            iterations += 1

    
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        suma = sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (M[i][n] - suma) / M[i][i]
        iterations += 1

    
    condicion_estimada = max(sum(abs(val) for val in row) for row in A)

    return x, iterations, condicion_estimada

# 3. Endpoint 
@app.post("/api/v1/elimination-gauss")
async def solve_gauss(data: MatrixInput):
    
    if len(data.A) != len(data.b) or any(len(row) != len(data.A) for row in data.A):
        raise HTTPException(status_code=400, detail="Las dimensiones de la matriz A y el vector b no coinciden.")

    start_time = time.perf_counter()
    
    try:
        solucion, iteraciones, condicion = gaussian_elimination(data.A, data.b)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
        
    end_time = time.perf_counter()
    tiempo_ejecucion = (end_time - start_time) * 1000 

    return {
        "metodo": "Eliminación de Gauss",
        "vector_solucion_x": solucion,
        "tiempo_ejecucion_ms": round(tiempo_ejecucion, 4),
        "iteraciones_reales": iteraciones,
        "numero_condicion_estimado": condicion
    }
