from src.gl import Renderer
import src.shaders as shaders

width = 1920
height = 1080
modelsFolder = 'models/'

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader  # type: ignore
rend.fragmentShader = shaders.fragmentShader  # type: ignore

# top view, top left translated
rend.glLoadModel(modelsFolder + 'phone.obj',
                 texturePath=modelsFolder + 'textures/phone.bmp',
                 translate=(width/2 - width/4, height/2 + height/4, 0), scale=(-1500, -1500, -1500), rotate=(90, 0, 180))

# bottom view, bottom right translated
rend.glLoadModel(modelsFolder + 'phone.obj',
                 texturePath=modelsFolder + 'textures/phone.bmp',
                 translate=(width/2 + width/4 + width/8, height/2 - height/4, 0), scale=(-1500, -1500, -1500), rotate=(270, 0, 180))


# left view, top right translated
rend.glLoadModel(modelsFolder + 'phone.obj',
                 texturePath=modelsFolder + 'textures/phone.bmp',
                 translate=(width/2 + width/4 - width/8 + width/20, height/2 + height/6, 0), scale=(-1500, -1500, -1500), rotate=(90, -120, 90))

# right view, bottom left translated
rend.glLoadModel(modelsFolder + 'phone.obj',
                 texturePath=modelsFolder + 'textures/phone.bmp',
                 translate=(width/2 - width/4 + width/8 + width/20, height/2 - height/6, 0), scale=(-1500, -1500, -1500), rotate=(200, 145, 90))

rend.glRender()

rend.glFinish('output.bmp')
