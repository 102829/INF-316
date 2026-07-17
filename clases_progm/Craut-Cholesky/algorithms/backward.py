def backward_substitution(U, y):

    n = len(U)

    x = [0.0] * n

    for i in range(n-1, -1, -1):

        suma = 0.0

        for j in range(i+1, n):

            suma += U[i][j] * x[j]

        x[i] = (
            y[i] - suma
        ) / U[i][i]

    return x