import math
from utils.emath import evector, ematrix


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

    if intensity < 0.5:
        intensity = 0.5

    b *= intensity*1.25
    g *= intensity*1.25
    r *= intensity*1.25

    return max(0, min(1, r)), max(0, min(1, g)), max(0, min(1, b))


def camouflage_shader(**kwargs):
    # this shader may have variables with rare names, but it's cause the initial idea was to make a toon shader

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


def fractal_shader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["tex_coords"]
    nA, nB, nC = kwargs["normals"]
    directional_light = kwargs["directional_light"]
    u, v, w = kwargs["barycentric_coords"]
    cam_matrix = kwargs["cam_matrix"]

    # Fractal parameters
    fractal_iterations = 100
    fractal_scale = 0.01

    # Calculate fractal value
    fractal_value = 0.0
    p = evector([u, v, w])
    for _ in range(fractal_iterations):
        p = evector([
            abs(p.data[0]) * fractal_scale + u,
            abs(p.data[1]) * fractal_scale + v,
            abs(p.data[2]) * fractal_scale + w
        ])
        fractal_value += math.sin(p.data[0] * p.data[1] + p.data[1]
                                  * p.data[2] + p.data[2] * p.data[0]) / fractal_iterations

    b = fractal_value
    g = fractal_value
    r = fractal_value

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

    b *= intensity * 1.5
    g *= intensity * 1.5
    r *= intensity * 1.5

    if intensity > 0:
        return r, g, b
    else:
        return (0, 0, 0)


def invert_shader(**kwargs):
    # this shader may have variables with rare names, but it's cause the initial idea was to make a retro anime shader

    texture = kwargs["texture"]
    tA, tB, tC = kwargs["tex_coords"]
    nA, nB, nC = kwargs["normals"]
    u, v, w = kwargs["barycentric_coords"]
    cam_matrix = kwargs["cam_matrix"]
    pixel_size = 2  # Increase this value to make the outline thicker

    cam_forward = evector(
        [cam_matrix.data[0][2], cam_matrix.data[1][2], cam_matrix.data[2][2]])

    # Calculate shading intensity (less affected by light)
    normal = evector([u * nA[0] + v * nB[0] + w * nC[0],
                      u * nA[1] + v * nB[1] + w * nC[1],
                      u * nA[2] + v * nB[2] + w * nC[2]])

    shading_intensity = normal.dot(cam_forward)

    # Retro shading color (invert texture if available)
    retro_shading_color = (1.0, 1.0, 1.0)  # Default white

    if texture is not None:
        tU = u * tA[0] + v * tB[0] + w * tC[0]
        tV = u * tA[1] + v * tB[1] + w * tC[1]
        texture_color = texture.get_color(tU, tV)
        retro_shading_color = (
            1.0 - texture_color[0],
            1.0 - texture_color[1],
            1.0 - texture_color[2]
        )

    # Outline effect
    cam_dot_normal = cam_forward.dot(normal)
    line_art_threshold = 0.2
    outline_thickness = 10

    if cam_dot_normal < line_art_threshold:
        retro_shading_color = (0.0, 0.0, 0.0)

    # Apply shading and return color
    retro_color = (
        max(0, min(1, retro_shading_color[0] * shading_intensity)),
        max(0, min(1, retro_shading_color[1] * shading_intensity)),
        max(0, min(1, retro_shading_color[2] * shading_intensity))
    )

    return retro_color


def normal_map_shader(**kwargs):
    texture = kwargs["texture"]
    tA, tB, tC = kwargs["tex_coords"]
    normal_map = kwargs["normal_map"]
    nA, nB, nC = kwargs["normals"]
    directional_light = kwargs["directional_light"]
    u, v, w = kwargs["barycentric_coords"]
    cam_matrix = kwargs["cam_matrix"]
    tangent = kwargs["tangent"]

    b = 1.0
    g = 1.0
    r = 1.0

    tU = u * tA[0] + v * tB[0] + w * tC[0]
    tV = u * tA[1] + v * tB[1] + w * tC[1]
    if texture is not None:

        texture_color = texture.get_color(tU, tV)
        b *= texture_color[2]
        g *= texture_color[1]
        r *= texture_color[0]

    normal = evector([u * nA[0] + v * nB[0] + w * nC[0],
                      u * nA[1] + v * nB[1] + w * nC[1],
                      u * nA[2] + v * nB[2] + w * nC[2]])

    if normal_map is not None:
        texture_normal = normal_map.get_color(tU, tV)
        texture_normal = evector([
            texture_normal[0] * 2 - 1,
            texture_normal[1] * 2 - 1,
            texture_normal[2] * 2 - 1
        ])
        texture_normal = texture_normal.normalize()

        bitangent = normal.cross(tangent)
        bitangent = bitangent.normalize()

        tangent = normal.cross(bitangent)
        tangent = tangent.normalize()

        tangent_matrix = ematrix([
            [tangent.data[0], bitangent.data[0], normal.data[0]],
            [tangent.data[1], bitangent.data[1], normal.data[1]],
            [tangent.data[2], bitangent.data[2], normal.data[2]]
        ])

        texture_normal = tangent_matrix @ texture_normal
        texture_normal = evector([
            texture_normal.data[0],
            texture_normal.data[1],
            texture_normal.data[2]
        ])
        texture_normal = texture_normal.normalize()
        intensity = texture_normal.dot(directional_light.negate())
    else:
        intensity = normal.dot(directional_light.negate())

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return (0, 0, 0)
