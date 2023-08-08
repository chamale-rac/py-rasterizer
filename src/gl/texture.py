from utils.efiles import bmp_texture


class Texture:
    """Class representing a BMP texture."""

    def __init__(self, path):
        """Initialize the Texture object.

        Args:
            path: The path to the BMP file.
        """
        self.path = path
        self.read()

    def read(self):
        """Read the BMP file and initialize the texture attributes."""
        self.pixels, self.width, self.height = bmp_texture(self.path)

    def get_color(self, u, v):
        """Get the color of the texture at the given (u, v) coordinates.

        Args:
            u: The u-coordinate.
            v: The v-coordinate.

        Returns:
            The color of the texture at the given coordinates if they lie within the texture boundaries, otherwise None.
        """
        if 0 <= u < 1 and 0 <= v < 1:
            x = int(u * self.width)
            y = int(v * self.height)
            return self.pixels[y][x]
        else:
            return None
