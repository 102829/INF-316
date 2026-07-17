from fastapi import FastAPI
from fastapi import HTTPException
from models import MatrixRequest

from algorithms.cholesky import cholesky_decomposition
from algorithms.forward import forward_substitution
from algorithms.backward import backward_substitution

from utils.validation import is_square, is_symmetric

import numpy as np
import time

app = FastAPI(
    title="Crout-Cholesky API",
    version="2.0.0",
    description="API para resolver sistemas lineales mediante el método de Cholesky"
)


@app.post("/api/v1/cholesky")
def solve(request: MatrixRequest):

    A = request.A
    b = request.b

    if not is_square(A):
        raise HTTPException(
            status_code=400,
            detail="La matriz no es cuadrada"
        )

    if not is_symmetric(A):
        raise HTTPException(
            status_code=400,
            detail="La matriz no es simétrica"
        )

    try:

        inicio = time.perf_counter()

        L = cholesky_decomposition(A)

        y = forward_substitution(L, b)

        LT = [
            [L[j][i] for j in range(len(L))]
            for i in range(len(L))
        ]

        x = backward_substitution(LT, y)

        fin = time.perf_counter()

        tiempo_ms = round((fin - inicio) * 1000, 6)

        condicion = round(
            float(
                np.linalg.cond(
                    np.array(A)
                )
            ),
            6
        )

        return {
    "version": "2.0",
    "success": True,
    "method": "Cholesky",
    "matrix_size": len(A),
    "execution_time_ms": tiempo_ms,
    "condition_number": condicion,
    "solution": x,
    "L": L
}

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )