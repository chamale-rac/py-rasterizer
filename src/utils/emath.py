import math


def is_close(a, b, rel_tol=1e-09):
    """Check whether two floating-point numbers are close to each other within a specified tolerance.

    Args:
        a: The first floating-point number.
        b: The second floating-point number.
        rel_tol: The relative tolerance. Defaults to 1e-09.

    Returns:
        True if the absolute difference between a and b is less than or equal to rel_tol times the larger of the absolute values of a and b, otherwise False.
    """
    return abs(a - b) <= rel_tol * max(abs(a), abs(b))


def barycentric_coords(A, B, C, P):
    """Compute the barycentric coordinates of a point P in a triangle ABC.

    Args:
        A: The coordinates of point A (x, y).
        B: The coordinates of point B (x, y).
        C: The coordinates of point C (x, y).
        P: The coordinates of point P (x, y).

    Returns:
        The barycentric coordinates of point P if it lies within the triangle ABC, otherwise None.
    """

    def area(a, b, c):
        """Compute the signed area of a triangle formed by three points."""
        return abs((a[0] * b[1] + b[0] * c[1] + c[0] * a[1]) - (a[1] * b[0] + b[1] * c[0] + c[1] * a[0]))

    areaABC = area(A, B, C)
    if areaABC == 0:
        return None

    areaPCB = area(P, C, B)
    areaACP = area(A, C, P)
    areaABP = area(A, B, P)

    u = areaPCB / areaABC
    v = areaACP / areaABC
    w = areaABP / areaABC

    if all(0 <= coord <= 1 for coord in (u, v, w)) and is_close(u + v + w, 1.0):
        return u, v, w
    else:
        return None


class Matrix:
    """
    Represents a matrix.
    """

    def __init__(self, data) -> None:
        """
        Initialize the Matrix object.

        Args:
            data: A list of lists representing the matrix.
        """
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])

    def __mul__(self, other) -> 'Matrix':
        """
        Multiply the matrix by another matrix or a scalar.

        Args:
            other: Another Matrix object or a scalar (int or float).

        Returns:
            The result of the multiplication as a new Matrix object.
        """
        if isinstance(other, Matrix):
            result = [[0] * other.cols for _ in range(self.rows)]
            for i in range(self.rows):
                for j in range(other.cols):
                    for k in range(self.cols):
                        result[i][j] += self.data[i][k] * other.data[k][j]
            return Matrix(result)
        elif isinstance(other, (int, float)):
            result = [[elem * other for elem in row] for row in self.data]
            return Matrix(result)

    def __matmul__(self, other) -> 'Vector':
        """
        Multiply the matrix by a vector (matrix-vector multiplication).

        Args:
            other: A Vector object.

        Returns:
            The result of the multiplication as a new Vector object.
        """
        if self.cols != len(other.data):
            raise ValueError("Matrix and vector dimensions are not compatible")

        result = [sum(self.data[i][j] * other.data[j]
                      for j in range(self.cols)) for i in range(self.rows)]
        return Vector(result)

    def __sub__(self, other) -> 'Matrix':
        """
        Subtract another matrix from this matrix.

        Args:
            other: Another Matrix object.

        Returns:
            The result of the subtraction as a new Matrix object.
        """
        result = [[self.data[i][j] - other.data[i][j]
                   for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(result)

    def invert(self) -> 'Matrix':
        """
        Calculate the inverse of the matrix using Gauss-Jordan elimination.

        Returns:
            The inverse of the matrix as a new Matrix object.
        """
        if self.rows != self.cols:
            raise ValueError("Matrix must be square for inversion")

        n = self.rows
        augmented_matrix = [[self.data[i][j] if j < n else 1 if j ==
                             i + n else 0 for j in range(2 * n)] for i in range(n)]

        # Perform Gauss-Jordan elimination
        for i in range(n):
            pivot = augmented_matrix[i][i]
            if pivot == 0:
                raise ValueError("Matrix is not invertible")

            for j in range(2 * n):
                augmented_matrix[i][j] /= pivot

            for k in range(n):
                if k != i:
                    factor = augmented_matrix[k][i]
                    for j in range(2 * n):
                        augmented_matrix[k][j] -= factor * \
                            augmented_matrix[i][j]

        inverted_data = [[augmented_matrix[i][j]
                          for j in range(n, 2 * n)] for i in range(n)]
        return Matrix(inverted_data)

    def __str__(self) -> str:
        """
        Return a string representation of the matrix.

        Returns:
            The string representation of the matrix.
        """
        return str(self.data)


class Vector:
    """
    Represents a vector.
    """

    def __init__(self, data) -> None:
        """
        Initialize the Vector object.

        Args:
            data: A list representing the vector.
        """
        self.data = data

    def __mul__(self, other) -> 'Vector':
        if isinstance(other, (int, float)):
            result = [elem * other for elem in self.data]
            return Vector(result)
        elif isinstance(other, Vector):
            if len(self.data) != len(other.data):
                raise ValueError(
                    "Vectors must have the same dimension for element-wise multiplication.")
            result = [self.data[i] * other.data[i]
                      for i in range(len(self.data))]
            return Vector(result)
        else:
            raise ValueError("Unsupported operand type for multiplication")

    def __rmul__(self, other) -> 'Vector':
        return self.__mul__(other)

    def __sub__(self, other) -> 'Vector':
        """
        Subtract another vector from this vector.

        Args:
            other: Another Vector object.

        Returns:
            The result of the subtraction as a new Vector object.
        """
        if isinstance(other, Vector):
            if len(self.data) != len(other.data):
                raise ValueError(
                    "Vectors must have the same dimension for subtraction.")
            result = [self.data[i] - other.data[i]
                      for i in range(len(self.data))]
            return Vector(result)
        else:
            raise ValueError("Unsupported operand type for subtraction")

    def normalize(self) -> 'Vector':
        """
        Calculate the normalized vector.

        Returns:
            The normalized vector as a new Vector object.
        """
        magnitude = math.sqrt(sum(elem ** 2 for elem in self.data))
        # Return a normalized vector as a new Vector object
        if magnitude != 0:
            return self * (1.0 / magnitude)
        else:
            return self

    def cross(self, other) -> 'Vector':
        """
        Calculate the cross product between this vector and another vector.

        Args:
            other: Another Vector object.

        Returns:
            The cross product as a new Vector object.
        """
        if len(self.data) != 3 or len(other.data) != 3:
            raise ValueError("Cross product is only defined for 3D vectors")

        result = [
            self.data[1] * other.data[2] - self.data[2] * other.data[1],
            self.data[2] * other.data[0] - self.data[0] * other.data[2],
            self.data[0] * other.data[1] - self.data[1] * other.data[0]
        ]

        return Vector(result)

    def __add__(self, other) -> 'Vector':
        """
        Add another vector or scalar value to this vector.

        Args:
            other: Another Vector object or scalar value.

        Returns:
            The result of the addition as a new Vector object.
        """
        if isinstance(other, Vector):
            if len(self.data) != len(other.data):
                raise ValueError(
                    "Vectors must have the same dimension for addition.")
            result = [self.data[i] + other.data[i]
                      for i in range(len(self.data))]
            return Vector(result)
        elif isinstance(other, (int, float)):
            result = [elem + other for elem in self.data]
            return Vector(result)
        else:
            raise ValueError("Unsupported operand type for addition")

    def dot(self, other) -> float:
        """
        Calculate the dot product between this vector and another vector.

        Args:
            other: Another Vector object.

        Returns:
            The dot product as a float.
        """
        if len(self.data) != len(other.data):
            raise ValueError(
                "Dot product is only defined for vectors of the same dimension")

        result = sum(self.data[i] * other.data[i]
                     for i in range(len(self.data)))
        return result

    def negate(self) -> 'Vector':
        """
        Return the negated vector.

        Returns:
            The negated vector as a new Vector object.
        """
        result = [-elem for elem in self.data]
        return Vector(result)


def ematrix(data) -> Matrix:
    """
    Create a new Matrix object.

    Args:
        data: A list of lists representing the matrix.

    Returns:
        A new Matrix object.
    """
    return Matrix(data)


def evector(data) -> Vector:
    """
    Create a new Vector object.

    Args:
        data: A list representing the vector.

    Returns:
        A new Vector object.
    """
    return Vector(data)
