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
    color = (1,1,1) 
    #(172/255, 243/255, 209/255)
    return color