def matrix_x_vector(matrix, vector):
    m_rows = len(matrix)
    m_cols = len(matrix[0])
    v_rows = len(vector)
    if m_cols != v_rows:
        raise ValueError("Matrix and vector dimensions do not match.")

    result = [0] * m_rows
    for i in range(m_rows):
        for j in range(v_rows):
            result[i] += matrix[i][j] * vector[j]

    return result


def matrix_x_matrix(a, b):
    # matrix multiplication function
    transposed_b = list(zip(*b))
    result_matrix = [[sum(element_a * element_b for element_a, element_b in zip(row_a, col_b))
                      for col_b in transposed_b]
                     for row_a in a]
    return result_matrix


def barycentricCoords(A, B, C, P):
    areaPCB = (B[1] - C[1]) * (P[0] - C[0]) + (C[0] - B[0]) * (P[1] - C[1])
    areaACP = (C[1] - A[1]) * (P[0] - C[0]) + (A[0] - C[0]) * (P[1] - C[1])
    areaABC = (B[1] - C[1]) * (A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1])

    # areaPBC = abs((P[0]*B[1] + B[0]*C[1] + C[0]*P[1]) -
    #               (P[1]*B[0] + B[1]*C[0] + C[1]*P[0]))

    # areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) -
    #               (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

    # areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) -
    #               (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = 1 - u - v

    return u, v, w
