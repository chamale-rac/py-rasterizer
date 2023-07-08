from gl import Renderer, V2, color
import random

width = 1920
height = 1080

rend = Renderer(width, height)


rend.glClearColor(0, 0, 0)
rend.glClear()

'''
# a point
rend.glColor(1, 1, 1)
rend.glPoint(1, 1)
'''

'''
# some lines
rend.glLine(V2(10, 10), V2(100, 100))
rend.glLine(V2(10, 10), V2(100, 50))
rend.glLine(V2(10, 10), V2(50, 100))
rend.glLine(V2(10, 10), V2(50, 50))
'''

'''
# one origin lines
for x in range(0, width, 10):
    rend.glLine(V2(0,0), V2(x, height-1))
'''

'''
# random color noise
for x in range(width):
    for y in range(height):
        if random.randint(0, 1) == 1:
            rend.glPoint(x, y, color(random.random(), random.random(), random.random()))
'''

for x in range(width):
    for y in range(height):
        if(random.random() > 0.995):
            size = random.randrange(0, 3)
            brightness = random.random() / 2 + 0.5 # ensure the range is 0.5 - 1

            starColor = color(brightness, brightness, brightness)
            if size == 0:
                rend.glPoint(x, y, starColor)
            elif size == 1:
                rend.glPoint(x, y, starColor)
                rend.glPoint(x + 1, y, starColor)
                rend.glPoint(x, y + 1, starColor)
                rend.glPoint(x - 1, y, starColor)
                rend.glPoint(x, y - 1, starColor)
            elif size == 2:
                rend.glPoint(x, y, starColor)
                rend.glPoint(x + 1, y, starColor)
                rend.glPoint(x, y + 1, starColor)
                rend.glPoint(x - 1, y, starColor)
                rend.glPoint(x, y - 1, starColor)
                rend.glPoint(x + 1, y + 1, starColor)
                rend.glPoint(x - 1, y - 1, starColor)
                rend.glPoint(x + 1, y - 1, starColor)
                rend.glPoint(x - 1, y + 1, starColor)

rend.glFinish('output.bmp')