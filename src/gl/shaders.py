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
    directional_light = kwargs["directional_light"]
    triangle_normal = kwargs["triangle_normal"]

    intensity = triangle_normal.dot(directional_light)

    color = (1, 1, 1)

    return color
