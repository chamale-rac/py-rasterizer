from gl import Renderer, V2, color
import random

width = 1920
height = 1080

rend = Renderer(width, height)

vertices = [
    V2(100, 100),
    V2(450, 275),
    V2(250, 500)
]

rend.glTriangle(vertices[0], vertices[1], vertices[2])

rend.glFinish('output.bmp')