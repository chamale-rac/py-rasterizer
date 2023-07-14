import struct # to convert data to bytes
from collections import namedtuple

V2 = namedtuple('Point2', ['x', 'y']) # 2D point

def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # 2 bytes
    return struct.pack('=h', w)

def dword(d):
    # 4 bytes
    return struct.pack('=l', d)

def color(r, g, b):
    # mul by 255 to get the color in bytes caus r, g, b are in range 0-1
    return bytes([int(b * 255), 
                  int(g * 255),
                  int(r * 255)])

class Renderer(object):
    # width and height of a frame
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.glClearColor(0, 0, 0)
        self.glClear()
        self.glColor(1, 1, 1)

    def glTriangle(self, v0, v1, v2, clr=None):
        self.glLine(v0, v1, clr)
        self.glLine(v1, v2, clr)
        self.glLine(v2, v0, clr)

    # determining the color of each pixel
    def glClearColor(self, r,g,b):
        self.clearColor = color(r,g,b)

    def glColor(self, r,g,b):
        self.currColor = color(r,g,b)

    # filling the frame with a single color
    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)] 
                       for x in range(self.width)]
        
    def glPoint(self, x, y, clr = None):
        if(x < self.width and x >= 0 and y < self.height and y >= 0): # check if the point is inside the frame
            self.pixels[int(x)][int(y)] = clr or self.currColor

    def glLine(self, v0, v1, clr = None):
        '''        
        # bresenham's line algorithm
        # y = mx + b
        m = (v1.y - v0.y) / (v1.x - v0.x)
        y = v0.y # the y value of the first point

        for x in range(v0.x, v1.x + 1):
            self.glPoint(x, int(y))
            y += m
        '''

        x0 = int(v0.x)
        x1 = int(v1.x)
        y0 = int(v0.y)
        y1 = int(v1.y)

        # check if the line is steep
        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y0)
            return
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        # if the line is steep, we transpose the image, it means rotating 90 degrees theoretically
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # if the initial point is bigger than the last point, we swap them
        if x0 > x1:    
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        limit = 0.5
        m = dy/dx
        y = y0
         
        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(int(y), x, clr or self.currColor)
            else:
                self.glPoint(x, int(y), clr or self.currColor)
            
            offset += m

            if offset >= limit:
                y += 1 if y0 < y1 else -1; limit += 1
        
    # generating the file, framebuffer, image    
    def glFinish(self, filename):
        with open(filename, 'wb') as file:
            # link to the format http://www.ece.ualberta.ca/~elliott/ee552/studentAppNotes/2003_w/misc/bmp_file_format/bmp_file_format.htm
            # header 
            file.write(char('B'))
            file.write(char('M'))
            file.write(dword(14 + 40 + self.width * self.height * 3)) # file size, 14 is the header size, 40 is the info header size and 3 is the number of bytes per pixel
            file.write(dword(0))
            file.write(dword(14 + 40)) # offset where the image starts

            # info header
            file.write(dword(40))
            file.write(dword(self.width))   
            file.write(dword(self.height))
            file.write(word(1)) # number of color planes, what is planes? like layers?
            file.write(word(24)) # number of bits per pixel, this will define the color depth
            file.write(dword(0)) # compression method
            file.write(dword(self.width * self.height * 3)) # raw image size

            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # color table, bitmap data
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])