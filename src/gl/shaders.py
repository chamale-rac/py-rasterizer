from utils.emath import evector


def vertex_shader(vertex, **kwargs):
    """Perform the vertex shader operation on a vertex.

    Args:
        vertex: The vertex coordinates (x, y, z).
        **kwargs: Additional keyword arguments.

    Returns:
        The transformed vertex coordinates after applying the vertex shader.
    """
    model_matrix = kwargs["model_matrix"]
    view_matrix = kwargs["view_matrix"]
    projection_matrix = kwargs["projection_matrix"]
    viewport_matrix = kwargs["viewport_matrix"]

    vt = evector([vertex[0], vertex[1], vertex[2], 1])
    vt = viewport_matrix * projection_matrix * view_matrix * model_matrix @ vt
    vt = evector([vt.data[0] / vt.data[3], vt.data[1] /
                 vt.data[3], vt.data[2] / vt.data[3]])

    return vt.data[:3]


def fragment_shader(**kwargs):
    """Perform the fragment shader operation on a pixel.

    Args:
        **kwargs: Additional keyword arguments.

    Returns:
        The color of the pixel after applying the fragment shader.
    """
    tex_coords = kwargs["tex_coords"]
    texture = kwargs["texture"]

    if texture is not None:
        color = texture.get_color(tex_coords[0], tex_coords[1])
    else:
        color = (1, 1, 1)

    return color


def flat_shader(**kwargs):
    tex_coords = kwargs["tex_coords"]
    texture = kwargs["texture"]
    directional_light = kwargs["directional_light"]
    triangle_normals = kwargs["normals"]

    b = 1.0
    g = 1.0
    r = 1.0

    if texture is not None:
        texture_color = texture.get_color(tex_coords[0], tex_coords[1])
        b *= texture_color[2]
        g *= texture_color[1]
        r *= texture_color[0]

    intensity = triangle_normals.dot(directional_light.negate())

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return (0, 0, 0)


def gouraud_shader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["tex_coords"]
    nA, nB, nC = kwargs["normals"]
    directional_light = kwargs["directional_light"]
    u, v, w = kwargs["barycentric_coords"]

    normal = evector([u * nA[0] + v * nB[0] + w * nC[0],
                      u * nA[1] + v * nB[1] + w * nC[1],
                      u * nA[2] + v * nB[2] + w * nC[2]])

    b = 1.0
    g = 1.0
    r = 1.0

    intensity = normal.dot(directional_light.negate())

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return (0, 0, 0)
