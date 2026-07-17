def crout_decomposition(A):

    n = len(A)

    L = [[0.0]*n for _ in range(n)]
    U = [[0.0]*n for _ in range(n)]

    for j in range(n):

        U[j][j] = 1.0

        for i in range(j, n):

            suma = 0.0

            for k in range(j):

                suma += (
                    L[i][k] *
                    U[k][j]
                )

            L[i][j] = A[i][j] - suma

        for i in range(j+1, n):

            suma = 0.0

            for k in range(j):

                suma += (
                    L[j][k] *
                    U[k][i]
                )

            U[j][i] = (
                A[j][i] - suma
            ) / L[j][j]

    return L, U