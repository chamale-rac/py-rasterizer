
from .obj import Obj
from .texture import Texture


class Model:
    def __init__(self, filename: str, texture_name: str, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):
        """
        Initialize the Model object.

        Args:
            filename (str): The name of the file containing the model.
            translate (tuple, optional): The translation values. Defaults to (0, 0, 0).
            rotate (tuple, optional): The rotation values. Defaults to (0, 0, 0).
            scale (tuple, optional): The scaling values. Defaults to (1, 1, 1).
        """
        self.load_model(filename)
        self.load_texture(texture_name)

        self.translate = translate
        self.rotate = rotate
        self.scale = scale

    def load_model(self, filename: str) -> None:
        """
        Load the model from the file.

        Args:
            filename (str): The name of the file containing the model.
        """
        model = Obj(filename)

        self.vertices = model.vertices
        self.tex_coords = model.tex_coords
        self.normals = model.normals
        self.faces = model.faces

    def load_texture(self, texture_name: str) -> None:
        """
        Load the texture for the model.

        Args:
            texture_name (str): The name of the texture.
        """
        self.texture = Texture(texture_name)
