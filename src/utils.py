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