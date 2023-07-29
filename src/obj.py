import re


class Obj(object):
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.lines = file.read().splitlines()

        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        for line in self.lines:
            try:
                # split the line in two, the first part is the key, the second part is the value
                prefix, value = re.split(r'\s+', line, 1)
            except:
                continue

            # value remove blank spaces at the beginning and at the end
            value = value.strip()
            # prefix por si acaso
            prefix = prefix.strip()

            if prefix == 'v':  # vertices
                # convert the string to float, each element of the list
                self.vertices.append(list(map(float, value.split(' '))))
            elif prefix == 'vt':  # texture coordinates
                # convert the string to float, each element of the list
                self.texcoords.append(list(map(float, value.split(' '))))
            elif prefix == 'vn':  # normals
                # convert the string to float, each element of the list
                self.normals.append(list(map(float, value.split(' '))))
            elif prefix == 'f':  # faces
                facesAppend = [list(map(int, vert.split('/')))
                               for vert in value.split(' ')]
                self.faces.append(facesAppend)
