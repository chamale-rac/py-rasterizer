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
                prefix, value = re.split(r'\s+', line, 1) # split the line in two, the first part is the key, the second part is the value
            except:
                continue
            
            #value remove blank spaces at the beginning and at the end
            value = value.strip() 
            # prefix por si acaso
            prefix = prefix.strip()

            if prefix == 'v': # vertices
                self.vertices.append(list(map(float, value.split(' ')))) # convert the string to float, each element of the list       
            elif prefix == 'vt': # texture coordinates
                self.texcoords.append(list(map(float, value.split(' ')))) # convert the string to float, each element of the list
            elif prefix == 'vn': # normals
                self.normals.append(list(map(float, value.split(' ')))) # convert the string to float, each element of the list
            elif prefix == 'f': # faces
                    facesAppend = [list(map(int, vert.split('/'))) for vert in value.split(' ')]
                    self.faces.append(facesAppend)
             