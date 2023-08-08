

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

    vt = [vertex[0], vertex[1], vertex[2], 1]
    vt = viewport_matrix * projection_matrix * view_matrix * model_matrix @ vt
    vt = vt.tolist()[0]
    vt = [vt[0] / vt[3], vt[1] / vt[3], vt[2] / vt[3]]

    return vt


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
