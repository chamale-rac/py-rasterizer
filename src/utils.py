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

# TODO check update formula on 28 jul class.


def barycentricCoords(A, B, C, P):
    areaABC = (B[1] - C[1]) * (A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1])

    if areaABC == 0:
        return 0, 0, 0

    areaPCB = (B[1] - C[1]) * (P[0] - C[0]) + (C[0] - B[0]) * (P[1] - C[1])
    areaACP = (C[1] - A[1]) * (P[0] - C[0]) + (A[0] - C[0]) * (P[1] - C[1])

    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = 1 - u - v

    return u, v, w
