from gl import Renderer, V2, V3, color
import shaders
import random
from obj import Obj

width = 1920
height = 1080

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader # type: ignore
rend.fragmentShader = shaders.fragmentShader # type: ignore

# verts = [V3(0,0,0),
#             V3(50,0,0),
#             V3(25,40,0)
#             ]

# rend.glAddVertices(verts)
# rend.glModelMatrix(translate=(width/2, height/2, 0))

rend.glLoadModel('model.obj', translate=(width/2, height/2, 0), scale=(400, 400, 400))

rend.glRender()

rend.glFinish('output.bmp')