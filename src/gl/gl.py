import numpy as np
from math import pi, sin, cos
from utils.estruct import color
from utils.emath import barycentric_coords
from utils.efiles import bmp_blend

from gl.model import Model

TRIANGLES = 2


class Renderer:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.clear_color = color(0, 0, 0)
        self.curr_color = color(1, 1, 1)
        self.objects = []
        self.vertex_shader = None
        self.fragment_shader = None
        self.primitive_type = TRIANGLES
        self.active_texture = None
        self.viewport(0, 0, width, height)
        self.cam_matrix()
        self.clear()

    def clear(self):
        self.pixels = [[self.clear_color for _ in range(self.height)]
                       for _ in range(self.width)]
        self.zbuffer = [[float('inf') for _ in range(self.height)]
                        for _ in range(self.width)]

    def set_clear_color(self, r: float, g: float, b: float):
        self.clear_color = color(r, g, b)

    def set_color(self, r: float, g: float, b: float):
        self.curr_color = color(r, g, b)

    def point(self, x: int, y: int, clr=None):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[x][y] = clr or self.curr_color

    def triangle(self, A, B, C, vtA, vtB, vtC):
        min_x = round(min(A[0], B[0], C[0]))
        max_x = round(max(A[0], B[0], C[0]))
        min_y = round(min(A[1], B[1], C[1]))
        max_y = round(max(A[1], B[1], C[1]))

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if 0 <= x < self.width and 0 <= y < self.height:
                    P = (x, y)
                    b_coords = barycentric_coords(A, B, C, P)

                    if b_coords is not None:
                        u, v, w = b_coords
                        z = u * A[2] + v * B[2] + w * C[2]

                        if z < self.zbuffer[x][y]:
                            self.zbuffer[x][y] = z
                            uvs = (u * vtA[0] + v * vtB[0] + w * vtC[0],
                                   u * vtA[1] + v * vtB[1] + w * vtC[1])

                            if self.fragment_shader is not None:
                                colorP = self.fragment_shader(
                                    tex_coords=uvs, texture=self.active_texture)
                                self.point(x, y, color(
                                    colorP[0], colorP[1], colorP[2]))
                            else:
                                self.point(x, y)

    def primitive_assembly(self, t_verts, t_tex_coords):
        primitives = []

        if self.primitive_type == TRIANGLES:
            for i in range(0, len(t_verts), 3):
                triangle = []
                for j in range(3):
                    triangle.append(t_verts[i + j])
                for j in range(3):
                    triangle.append(t_tex_coords[i + j])
                primitives.append(triangle)

        return primitives

    def viewport(self, x, y, width, height):
        """Sets the viewport to render the image.

        Args:
            x (int): X coordinate of the viewport.
            y (int): Y coordinate of the viewport.
            width (int): Width of the viewport.
            height (int): Height of the viewport.
        """
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_width = width
        self.viewport_height = height

    def cam_matrix(self, translate=(0, 0, 0), rotate=(0, 0, 0)):
        """Builds the camera matrix and its inverse (view matrix).

        Args:
            translate (tuple, optional): Translation vector. Defaults to (0, 0, 0).
            rotate (tuple, optional): Rotation vector. Defaults to (0, 0, 0).
        """
        self.cam_matrix = self.model_matrix(translate, rotate)
        self.view_matrix = np.linalg.inv(self.cam_matrix)

    def model_matrix(self, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):
        translation = np.matrix([[1, 0, 0, translate[0]],
                                 [0, 1, 0, translate[1]],
                                 [0, 0, 1, translate[2]],
                                 [0, 0, 0, 1]])

        rot_mat = self.rotation_matrix(rotate[0], rotate[1], rotate[2])

        scale_mat = np.matrix([[scale[0], 0, 0, 0],
                              [0, scale[1], 0, 0],
                              [0, 0, scale[2], 0],
                              [0, 0, 0, 1]])

        return translation * rot_mat * scale_mat

    def rotation_matrix(self, pitch=0, yaw=0, roll=0):
        pitch *= pi / 180
        yaw *= pi / 180
        roll *= pi / 180

        rotation_x = np.matrix([[1, 0, 0, 0],
                                [0, cos(pitch), -sin(pitch), 0],
                                [0, sin(pitch), cos(pitch), 0],
                                [0, 0, 0, 1]])

        rotation_y = np.matrix([[cos(yaw), 0, sin(yaw), 0],
                                [0, 1, 0, 0],
                                [-sin(yaw), 0, cos(yaw), 0],
                                [0, 0, 0, 1]])

        rotation_z = np.matrix([[cos(roll), -sin(roll), 0, 0],
                                [sin(roll), cos(roll), 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])

        return rotation_x * rotation_y * rotation_z

    def line(self, v0, v1, clr=None):

        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])

        if x0 == x1 and y0 == y1:
            self.point(x0, y0)
            return

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

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
                self.point(y, x, clr or self.currColor)
            else:
                self.point(x, y, clr or self.currColor)

            offset += m

            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1

                limit += 1

    def gl_load_model(self, filename, texture_name, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):
        model = Model(filename, texture_name, translate, rotate, scale)

        self.objects.append(model)

    def gl_render(self):

        transformed_verts = []
        tex_coords = []

        for model in self.objects:

            self.active_texture = model.texture
            mMat = self.model_matrix(
                model.translate, model.rotate, model.scale)

            for face in model.faces:
                vertCount = len(face)

                v0 = model.vertices[face[0][0] - 1]
                v1 = model.vertices[face[1][0] - 1]
                v2 = model.vertices[face[2][0] - 1]
                if vertCount == 4:
                    v3 = model.vertices[face[3][0] - 1]

                if self.vertex_shader:
                    v0 = self.vertex_shader(v0, model_matrix=mMat)
                    v1 = self.vertex_shader(v1, model_matrix=mMat)
                    v2 = self.vertex_shader(v2, model_matrix=mMat)
                    if vertCount == 4:
                        v3 = self.vertex_shader(v3, model_matrix=mMat)

                transformed_verts.append(v0)
                transformed_verts.append(v1)
                transformed_verts.append(v2)
                if vertCount == 4:
                    transformed_verts.append(v0)
                    transformed_verts.append(v2)
                    transformed_verts.append(v3)

                vt0 = model.tex_coords[face[0][1] - 1]
                vt1 = model.tex_coords[face[1][1] - 1]
                vt2 = model.tex_coords[face[2][1] - 1]
                if vertCount == 4:
                    vt3 = model.tex_coords[face[3][1] - 1]

                tex_coords.append(vt0)
                tex_coords.append(vt1)
                tex_coords.append(vt2)
                if vertCount == 4:
                    tex_coords.append(vt0)
                    tex_coords.append(vt2)
                    tex_coords.append(vt3)

        primitives = self.primitive_assembly(transformed_verts, tex_coords)

        for prim in primitives:
            if self.primitive_type == TRIANGLES:
                self.triangle(prim[0], prim[1], prim[2],
                              prim[3], prim[4], prim[5])

    def gl_finish(self, filename):
        bmp_blend(filename, self.width, self.height, self.pixels)
