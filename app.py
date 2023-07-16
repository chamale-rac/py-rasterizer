from gl import Renderer, V2, V3, color
import shaders
import random
from obj import Obj

width = 1920
height = 1080
modelsFolder = 'models/'

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader # type: ignore
rend.fragmentShader = shaders.fragmentShader # type: ignore

rend.glLoadModel( modelsFolder + 'goose.obj', translate=(width/2 - 170, height/2 - 112, 0), scale=(50, 50, 50), rotate=(40, 40, 35))

rend.glLoadModel( modelsFolder + 'plane.obj', translate=(width/2- 
150, height/2-100, 0), scale=(1700, 1700, 1700), rotate=(40, 50, 40))

rend.glRender()

rend.glFinish('output.bmp')