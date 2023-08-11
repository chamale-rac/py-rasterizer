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
    cam_matrix = kwargs["cam_matrix"]

    b = 1.0
    g = 1.0
    r = 1.0

    if texture is not None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]

        texture_color = texture.get_color(tU, tV)
        b *= texture_color[2]
        g *= texture_color[1]
        r *= texture_color[0]

    normal = evector([u * nA[0] + v * nB[0] + w * nC[0],
                      u * nA[1] + v * nB[1] + w * nC[1],
                      u * nA[2] + v * nB[2] + w * nC[2]])

    intensity = normal.dot(directional_light.negate())

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return (0, 0, 0)


def toon_shader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["tex_coords"]
    nA, nB, nC = kwargs["normals"]
    directional_light = kwargs["directional_light"]
    u, v, w = kwargs["barycentric_coords"]
    cam_matrix = kwargs["cam_matrix"]
    pixel_size = 2  # Increase this value to make the outline thicker

    cam_forward = evector(
        [cam_matrix.data[0][2], cam_matrix.data[1][2], cam_matrix.data[2][2]])

    # Define the toon shading levels and their corresponding metallic colors
    shading_levels = [0.0, 0.3, 0.6, 0.9]
    shading_colors = [
        (0.2, 0.2, 0.2),  # Level 0: Dark Gray (Metallic)
        (0.08, 0.31, 0.53),  # Dark Blue
        (0.93, 0.29, 0.34),  # Red
        (0.92, 0.85, 0.49)   # Light Yellow
    ]

    if texture is not None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]

        texture_color = texture.get_color(tU, tV)
        b = texture_color[2]
        g = texture_color[1]
        r = texture_color[0]
    else:
        b = 1.0
        g = 1.0
        r = 1.0

    normal = evector([u * nA[0] + v * nB[0] + w * nC[0],
                      u * nA[1] + v * nB[1] + w * nC[1],
                      u * nA[2] + v * nB[2] + w * nC[2]])

    intensity = normal.dot(directional_light.negate())

    shading_level = 0
    for level, threshold in enumerate(shading_levels):
        if intensity >= threshold:
            shading_level = level

    toon_shading_color = shading_colors[shading_level]

    cam_dot_normal = cam_forward.dot(normal)

    line_art_threshold = 0.2
    outline_thickness = 10

    if cam_dot_normal < line_art_threshold:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue

                modified_normal = normal + \
                    evector([dx, dy, 0]) * (outline_thickness * pixel_size)

                neighbor_cam_dot_normal = cam_forward.dot(modified_normal)

                if neighbor_cam_dot_normal < line_art_threshold:
                    toon_shading_color = (0.0, 0.0, 0.0)
                    break

    # Calculate the influence of the light intensity on texture blending
    light_influence = intensity  # Adjust this for desired influence strength

    # Calculate the final color by blending toon shading, texture, and light intensity
    texture_mix_factor = 0.3  # Adjust this factor for the desired texture blending
    final_color = (
        max(0, min(1, (r * (1 - texture_mix_factor) +
            toon_shading_color[0] * texture_mix_factor) * light_influence)),
        max(0, min(1, (g * (1 - texture_mix_factor) +
            toon_shading_color[1] * texture_mix_factor) * light_influence)),
        max(0, min(1, (b * (1 - texture_mix_factor) +
            toon_shading_color[2] * texture_mix_factor) * light_influence))
    )

    return final_color
