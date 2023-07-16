import random as rd

def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs['modelMatrix']

    vt = [vertex[0], 
                         vertex[1],
                         vertex[2],
                        1]

    vt = modelMatrix @ vt

    vt = vt.tolist()[0]

    vt = [vt[0]/vt[3],
          vt[1]/vt[3],
          vt[2]/vt[3]]
    # in the future there will be some work here
    return vt

def getRandomFragmentShader(**kwargs):
    # with random colors between 0.5 and 1
    a = 0.5
    b = 1
    color = [rd.uniform(a, b), rd.uniform(a, b), rd.uniform(a, b)]
    # cool color: (172, 243, 209)
    return color

def fragmentShader(**kwargs):
    color = (172/255, 243/255, 209/255)
    return color