from src.gl import Renderer
import src.shaders as shaders

width = 1920
height = 1080
modelsFolder = 'models/'

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader  # type: ignore
rend.fragmentShader = shaders.fragmentShader  # type: ignore

rend.glLoadModel(modelsFolder + 'face.obj',
                 texturePath=modelsFolder + 'textures/face.bmp',
                 translate=(width/2 -
                            170, height/2 - 112, 0), scale=(400, 400, 400), rotate=(40, 40, 35))

rend.glLoadModel(modelsFolder + 'face.obj',
                 texturePath=modelsFolder + 'textures/face.bmp',
                 translate=(width/4 -
                            170, height/4 - 112, 0), scale=(400, 400, 400), rotate=(40, 90, 35))

# rend.glLoadModel(modelsFolder + 'plane.obj', translate=(width/2 -
#                                                         150, height/2-100, 0), scale=(1700, 1700, 1700), rotate=(40, 50, 40))

rend.glRender()


# triangle = [(100, 100), (250, 400), (400, 100)]

# rend.glTriangle_bc(triangle[0], triangle[1], triangle[2])

rend.glFinish('output.bmp')
