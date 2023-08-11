import numpy as np
from math import pi, sin, cos, tan
from utils.estruct import color
from utils.emath import barycentric_coords, ematrix, evector
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
        self.projection_matrix()
        self.clear()
        self.directional_light = (1, 0, 0)

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
                                triangle_normal = (
                                    evector(B) - evector(A)).cross(evector(C) - evector(A))
                                # triangle_normal = np.cross(np.subtract(B,A), np.subtract(C,A))
                                triangle_normal = triangle_normal.normalize()
                                # triangle_normal = triangle_normal / np.linalg.norm(triangle_normal)

                                colorP = self.fragment_shader(
                                    tex_coords=uvs,
                                    texture=self.active_texture,
                                    triangle_normal=triangle_normal,
                                    directional_light=self.directional_light)
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

        self.viewport_matrix = ematrix([[width/2, 0, 0, x + width/2],
                                        [0, height/2, 0, y + height/2],
                                        [0, 0, 0.5, 0.5],
                                        [0, 0, 0, 1]])

    def look_at(self, cam_pos=(0, 0, 0), eye_pos=(0, 0, 0), rotateZ=0):
        """Sets the camera position, eye position, and rotation.

        Args:
            cam_pos (tuple, optional): Camera position. Defaults to (0,0,0).
            eye_pos (tuple, optional): Eye position. Defaults to (0,0,0).
            rotate (tuple, optional): Rotation angles in degrees (pitch, yaw, roll). Defaults to (0,0,0).
        """
        import math

        pitch, yaw, roll = map(math.radians, (0, 0, rotateZ))

        world_up = evector([0, 1, 0])

        forward = evector(cam_pos) - evector(eye_pos)
        forward = forward.normalize()

        right = world_up.cross(forward)
        right = right.normalize()

        up = forward.cross(right)
        up = up.normalize()

        rotation_matrix = ematrix([
            [math.cos(yaw) * math.cos(roll), math.cos(yaw)
             * math.sin(roll), -math.sin(yaw), 0],
            [math.sin(pitch) * math.sin(yaw) * math.cos(roll) - math.cos(pitch) * math.sin(roll),
             math.sin(pitch) * math.sin(yaw) * math.sin(roll) + math.cos(pitch) * math.cos(roll), math.sin(pitch) * math.cos(yaw), 0],
            [math.cos(pitch) * math.sin(yaw) * math.cos(roll) + math.sin(pitch) * math.sin(roll),
             math.cos(pitch) * math.sin(yaw) * math.sin(roll) - math.sin(pitch) * math.cos(roll), math.cos(pitch) * math.cos(yaw), 0],
            [0, 0, 0, 1]
        ])

        self.cam_matrix = rotation_matrix * ematrix([
            [right.data[0], up.data[0], forward.data[0], cam_pos[0]],
            [right.data[1], up.data[1], forward.data[1], cam_pos[1]],
            [right.data[2], up.data[2], forward.data[2], cam_pos[2]],
            [0, 0, 0, 1]
        ])

        self.view_matrix = self.cam_matrix.invert()

    def cam_matrix(self, translate=(0, 0, 0), rotate=(0, 0, 0)):
        """Builds the camera matrix and its inverse (view matrix).

        Args:
            translate (tuple, optional): Translation vector. Defaults to (0, 0, 0).
            rotate (tuple, optional): Rotation vector. Defaults to (0, 0, 0).
        """
        self.cam_matrix = self.model_matrix(translate, rotate)
        self.view_matrix = self.cam_matrix.invert()

    def projection_matrix(self, n=0.1, f=1000, fov=60):
        """Builds the projection matrix.

        Args:
            n (float, optional): Near plane. Defaults to 0.1.
            f (int, optional): Far plane. Defaults to 1000.
            fov (int, optional): Field of view. Defaults to 60.

        Returns:
            aspect_ratio (float): Aspect ratio of the viewport.
            t (float): Top plane.
            r (float): Right plane.
        """
        aspect_ratio = self.viewport_width / self.viewport_height
        t = tan((fov * pi / 180) / 2) * n
        r = t * aspect_ratio

        self.projection_matrix = ematrix([[n/r, 0, 0, 0],
                                          [0, n/t, 0, 0],
                                          [0, 0, -(f+n)/(f-n), -
                                           (2*f*n)/(f-n)],
                                          [0, 0, -1, 0]])

    def model_matrix(self, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):
        translation = ematrix([[1, 0, 0, translate[0]],
                               [0, 1, 0, translate[1]],
                               [0, 0, 1, translate[2]],
                               [0, 0, 0, 1]])

        rot_mat = self.rotation_matrix(rotate[0], rotate[1], rotate[2])

        scale_mat = ematrix([[scale[0], 0, 0, 0],
                             [0, scale[1], 0, 0],
                             [0, 0, scale[2], 0],
                             [0, 0, 0, 1]])

        return translation * rot_mat * scale_mat

    def rotation_matrix(self, pitch=0, yaw=0, roll=0):
        pitch *= pi / 180
        yaw *= pi / 180
        roll *= pi / 180

        rotation_x = ematrix([[1, 0, 0, 0],
                              [0, cos(pitch), -sin(pitch), 0],
                              [0, sin(pitch), cos(pitch), 0],
                              [0, 0, 0, 1]])

        rotation_y = ematrix([[cos(yaw), 0, sin(yaw), 0],
                              [0, 1, 0, 0],
                              [-sin(yaw), 0, cos(yaw), 0],
                              [0, 0, 0, 1]])

        rotation_z = ematrix([[cos(roll), -sin(roll), 0, 0],
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
            model_matrix = self.model_matrix(
                model.translate, model.rotate, model.scale)

            for face in model.faces:
                vertCount = len(face)

                v0 = model.vertices[face[0][0] - 1]
                v1 = model.vertices[face[1][0] - 1]
                v2 = model.vertices[face[2][0] - 1]
                if vertCount == 4:
                    v3 = model.vertices[face[3][0] - 1]

                if self.vertex_shader:
                    v0 = self.vertex_shader(v0, model_matrix=model_matrix, view_matrix=self.view_matrix,
                                            projection_matrix=self.projection_matrix, viewport_matrix=self.viewport_matrix)
                    v1 = self.vertex_shader(v1, model_matrix=model_matrix, view_matrix=self.view_matrix,
                                            projection_matrix=self.projection_matrix, viewport_matrix=self.viewport_matrix)
                    v2 = self.vertex_shader(v2, model_matrix=model_matrix, view_matrix=self.view_matrix,
                                            projection_matrix=self.projection_matrix, viewport_matrix=self.viewport_matrix)
                    if vertCount == 4:
                        v3 = self.vertex_shader(v3, model_matrix=model_matrix, view_matrix=self.view_matrix,
                                                projection_matrix=self.projection_matrix, viewport_matrix=self.viewport_matrix)

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
