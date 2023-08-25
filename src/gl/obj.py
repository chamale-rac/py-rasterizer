from utils.efiles import obj_model


class Obj(object):
    """A class for loading and parsing OBJ files."""

    def __init__(self, path):
        """Initialize the object.

        Args:
            filename: The name of the OBJ file to load.
        """
        self.path = path
        self.read()

    def read(self):
        """Read the OBJ file.

        Returns:
            A tuple containing the vertex, texture coordinate, normal, and face data.
        """
        self.vertices, self.tex_coords, self.normals, self.faces = obj_model(
            self.path)
