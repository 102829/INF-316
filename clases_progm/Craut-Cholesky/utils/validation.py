def is_square(A):
    n = len(A)
    return all(len(row) == n for row in A)

def is_symmetric(A):
    n = len(A)

    for i in range(n):
        for j in range(n):
            if abs(A[i][j] - A[j][i]) > 1e-9:
                return False

    return True