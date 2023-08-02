import struct  # to convert data to bytes
from collections import namedtuple
import math  # the teacher allows just this external library
from .obj import Obj
from .utils import matrix_x_matrix, barycentricCoords
from .texture import Texture

V2 = namedtuple('Point2', ['x', 'y'])  # 2D point
V3 = namedtuple('Point2', ['x', 'y', 'z'])  # 3D point

POINTS = 0
LINES = 1
TRIANGLES = 2
QUADS = 3


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


class Model(object):
    def __init__(self, filename, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):

        model = Obj(filename)

        self.vertices = model.vertices
        self.faces = model.faces
        self.normals = model.normals
        self.texcoords = model.texcoords

        self.translate = translate
        self.rotate = rotate
        self.scale = scale

    def LoadTexture(self, path):
        self.texture = Texture(path)


class Renderer(object):
    # width and height of a frame
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.glClearColor(0, 0, 0)
        self.glClear()
        self.glColor(1, 1, 1)

        self.objects = []

        self.vertexShader = None
        self.fragmentShader = None

        self.primitiveType = TRIANGLES
        self.vertexBuffer = []

        self.activeTexture = None

    def glTriangle(self, v0, v1, v2, clr=None):
        self.glLine(v0, v1, clr or self.currColor)
        self.glLine(v1, v2, clr or self.currColor)
        self.glLine(v2, v0, clr or self.currColor)

    def glTriangle_bc(self, A, B, C, vtA, vtB, vtC):
        minX = round(min(A[0], B[0], C[0]))
        maxX = round(max(A[0], B[0], C[0]))
        minY = round(min(A[1], B[1], C[1]))
        maxY = round(max(A[1], B[1], C[1]))

        colorA = (1, 0, 0)
        colorB = (0, 1, 0)
        colorC = (0, 0, 1)

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                P = (x, y)
                u, v, w = barycentricCoords(A, B, C, P)

                if 0 <= u <= 1 and 0 <= v <= 1 and 0 <= w <= 1:
                    z = u * A[2] + v * B[2] + w * C[2]

                    try:
                        zget = self.zbuffer[x][y]
                    except:
                        zget = None

                    if zget != None:
                        if z < zget:
                            self.zbuffer[x][y] = z

                            uvs = (vtA[0] * u + vtB[0] * v + vtC[0] * w,
                                   vtA[1] * u + vtB[1] * v + vtC[1] * w)

                            if self.fragmentShader != None:
                                colorP = self.fragmentShader(
                                    texCoords=uvs, texture=self.activeTexture)

                                self.glPoint(x, y, color(
                                    colorP[0], colorP[1], colorP[2]))
                            else:
                                self.glPoint(x, y, colorP)

    def glModelMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
        translation = [[1, 0, 0, translate[0]],
                       [0, 1, 0, translate[1]],
                       [0, 0, 1, translate[2]],
                       [0, 0, 0, 1]]
        scaleMat = [[scale[0], 0, 0, 0],
                    [0, scale[1], 0, 0],
                    [0, 0, scale[2], 0],
                    [0, 0, 0, 1]]

        rx = math.radians(rotate[0])
        ry = math.radians(rotate[1])
        rz = math.radians(rotate[2])

        cosrx, sinrx = math.cos(rx), math.sin(rx)
        cosry, sinry = math.cos(ry), math.sin(ry)
        cosrz, sinrz = math.cos(rz), math.sin(rz)

        # assemble rotation matrices
        rotx = [[1, 0, 0, 0],
                [0, cosrx, -sinrx, 0],
                [0, sinrx, cosrx, 0],
                [0, 0, 0, 1]]

        roty = [[cosry, 0, sinry, 0],
                [0, 1, 0, 0],
                [-sinry, 0, cosry, 0],
                [0, 0, 0, 1]]

        rotz = [[cosrz, -sinrz, 0, 0],
                [sinrz, cosrz, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]]

    # combine rotation matrices
        rotation = matrix_x_matrix(rotz, matrix_x_matrix(roty, rotx))

    # combine translation, scale, and rotation matrices
        return matrix_x_matrix(translation, matrix_x_matrix(rotation, scaleMat))

    def glAddVertices(self, vertices):
        for vertex in vertices:
            self.vertexBuffer.append(vertex)

    def glPrimitiveAssembly(self, tVertices, tTexCoords):

        primitives = []

        # convert the vertices to triangles
        if self.primitiveType == TRIANGLES:
            for i in range(0, len(tVertices), 3):
                triangle = []

                # Vertices
                triangle.append(tVertices[i])
                triangle.append(tVertices[i+1])
                triangle.append(tVertices[i+2])

                # TexCoords
                triangle.append(tTexCoords[i])
                triangle.append(tTexCoords[i+1])
                triangle.append(tTexCoords[i+2])

                primitives.append(triangle)
        return primitives

    # determining the color of each pixel
    def glClearColor(self, r, g, b):
        self.clearColor = color(r, g, b)

    def glColor(self, r, g, b):
        self.currColor = color(r, g, b)

    # filling the frame with a single color
    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)]
                       for x in range(self.width)]

        self.zbuffer = [[float('inf') for y in range(self.height)]
                        for x in range(self.width)]

    def glPoint(self, x, y, clr=None):
        # check if the point is inside the frame
        if (x < self.width and x >= 0 and y < self.height and y >= 0):
            self.pixels[int(x)][int(y)] = clr or self.currColor

    def glLine(self, v0, v1, clr=None):
        '''        
        # bresenham's line algorithm
        # y = mx + b
        m = (v1.y - v0.y) / (v1.x - v0.x)
        y = v0.y # the y value of the first point

        for x in range(v0.x, v1.x + 1):
            self.glPoint(x, int(y))
            y += m
        '''

        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])

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
                y += 1 if y0 < y1 else -1
                limit += 1

    # generating the file, framebuffer, image
    def glFinish(self, filename):
        with open(filename, 'wb') as file:
            # link to the format http://www.ece.ualberta.ca/~elliott/ee552/studentAppNotes/2003_w/misc/bmp_file_format/bmp_file_format.htm
            # header
            file.write(char('B'))
            file.write(char('M'))
            # file size, 14 is the header size, 40 is the info header size and 3 is the number of bytes per pixel
            file.write(dword(14 + 40 + self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(14 + 40))  # offset where the image starts

            # info header
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            # number of color planes, what is planes? like layers?
            file.write(word(1))
            # number of bits per pixel, this will define the color depth
            file.write(word(24))
            file.write(dword(0))  # compression method
            file.write(dword(self.width * self.height * 3))  # raw image size

            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # color table, bitmap data
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])

    def glLoadModel(self, filename, texturePath, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):

        model = Model(filename, translate, rotate, scale)
        model.LoadTexture(texturePath)
        self.objects.append(model)

    def glRender(self):
        transformedVertices = []
        textureCoords = []

        count = 0
        for model in self.objects:
            self.activeTexture = model.texture

            mMat = self.glModelMatrix(
                model.translate, model.scale, model.rotate)
            for face in model.faces:
                vertCount = len(face)
                v0 = model.vertices[face[0][0] - 1]
                v1 = model.vertices[face[1][0] - 1]
                v2 = model.vertices[face[2][0] - 1]
                if vertCount == 4:
                    v3 = model.vertices[face[3][0] - 1]

                # aqui no debo enviar uno por uno
                if self.vertexShader:
                    v0 = self.vertexShader(v0, modelMatrix=mMat)
                    v1 = self.vertexShader(v1, modelMatrix=mMat)
                    v2 = self.vertexShader(v2, modelMatrix=mMat)
                    if vertCount == 4:
                        v3 = self.vertexShader(
                            v3, modelMatrix=mMat)  # type: ignore

                transformedVertices.append(v0)
                transformedVertices.append(v1)
                transformedVertices.append(v2)
                if vertCount == 4:
                    transformedVertices.append(v0)
                    transformedVertices.append(v2)
                    transformedVertices.append(v3)  # type: ignore

                vt0 = model.texcoords[face[0][1] - 1]
                vt1 = model.texcoords[face[1][1] - 1]
                vt2 = model.texcoords[face[2][1] - 1]
                if vertCount == 4:
                    vt3 = model.texcoords[face[3][1] - 1]

                textureCoords.append(vt0)
                textureCoords.append(vt1)
                textureCoords.append(vt2)
                if vertCount == 4:
                    textureCoords.append(vt0)
                    textureCoords.append(vt2)
                    textureCoords.append(vt3)

        primitives = self.glPrimitiveAssembly(
            transformedVertices, textureCoords)

        # primColor = None
        # if self.fragmentShader:
        #     primColor = self.fragmentShader()
        #     primColor = color(primColor[0], primColor[1], primColor[2])
        # else:
        #     primColor = self.currColor

        for prim in primitives:
            if self.primitiveType == TRIANGLES:
                # first 3 vertices are the triangle
                # next 3 correspond to the texture coordinates
                self.glTriangle_bc(prim[0], prim[1], prim[2],
                                   prim[3], prim[4], prim[5])
