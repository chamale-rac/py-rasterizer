from gl import Renderer

width = 520
height = 320

rend = Renderer(width, height)


rend.glClearColor(0, 0, 0)
rend.glClear()

rend.glColor(1, 1, 1)
rend.glPoint(1, 1)

rend.glFinish('output.bmp')