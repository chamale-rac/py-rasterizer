def factorial(n):
    """Compute the factorial of a number.

    Args:
        n: The number to compute the factorial of.

    Returns:
        The factorial of n.
    """
    return 1 if n == 0 else n * factorial(n - 1)


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


def pi(n=10000):
    """Compute an approximation of pi using the Leibniz formula.

    Args:
        n: The number of terms to use in the series. Defaults to 10000.

    Returns:
        An approximation of pi.

    References:
        https://proofwiki.org/wiki/Leibniz%27s_Formula_for_Pi
    """
    return 4 * sum((-1) ** k / (2 * k + 1) for k in range(n))


def sin(x, n=100):
    """Compute an approximation of sin(x) using power series.

    Args:
        x: The angle in radians.
        n: The number of terms to use in the series. Defaults to 100.

    Returns:
        An approximation of sin(x).

    References:
        https://proofwiki.org/wiki/Power_Series_Expansion_for_Sine_Function
    """
    return sum((-1) ** k * x ** (2 * k + 1) / factorial(2 * k + 1) for k in range(n))


def cos(x, n=100):
    """Compute an approximation of cos(x) using power series.

    Args:
        x: The angle in radians.
        n: The number of terms to use in the series. Defaults to 100.

    Returns:
        An approximation of cos(x).

    References:
        https://proofwiki.org/wiki/Power_Series_Expansion_for_Cosine_Function
    """
    return sum((-1)**k * x**(2*k) / factorial(2*k) for k in range(n))
