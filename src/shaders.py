from .utils import matrix_x_vector


def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs['modelMatrix']

    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]

    vt = matrix_x_vector(modelMatrix, vt)

    vt = [vt[i]/vt[3] for i in range(3)]
    # in the future there will be some work here
    return vt


def fragmentShader(**kwargs):
    texCoords = kwargs['texCoords']
    texture = kwargs['texture']

    if texture != None:
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (1, 1, 1)
    return color
