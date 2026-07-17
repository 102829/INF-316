def forward_substitution(L, b):

    n = len(L)

    y = [0.0] * n

    for i in range(n):

        suma = 0.0

        for j in range(i):
            suma += L[i][j] * y[j]

        y[i] = (
            b[i] - suma
        ) / L[i][i]

    return y