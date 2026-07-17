import math

def cholesky_decomposition(A):
    n = len(A)

    L = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):

        for j in range(i + 1):

            suma = 0.0

            for k in range(j):
                suma += L[i][k] * L[j][k]

            if i == j:

                valor = A[i][i] - suma

                if valor <= 0:
                    raise ValueError(
                        "La matriz no es definida positiva"
                    )

                L[i][j] = math.sqrt(valor)

            else:

                L[i][j] = (
                    A[i][j] - suma
                ) / L[j][j]

    return L