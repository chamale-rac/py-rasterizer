import re
import struct
from .estruct import char, dword, word


def bmp_blend(filename, width, height, pixels):
    """Write a BMP file with the specified pixel data.

    Args:
        filename: The name of the BMP file to write.
        width: The width of the image in pixels.
        height: The height of the image in pixels.
        pixels: A list of lists of RGB tuples representing the pixel data.
    """
    with open(filename, "wb") as file:
        # BMP header
        file.write(char("B"))
        file.write(char("M"))
        file.write(dword(14 + 40 + (width * height * 3)))
        file.write(dword(0))
        file.write(dword(14 + 40))

        # DIB header
        file.write(dword(40))
        file.write(dword(width))
        file.write(dword(height))
        file.write(word(1))
        file.write(word(24))
        file.write(dword(0))
        file.write(dword(width * height * 3))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))

        # Pixel data
        for y in range(height):
            for x in range(width):
                file.write(pixels[x][y])

    print(f"File {filename} written successfully.")


def bmp_texture(filename):
    """Read a BMP file and return its pixel data. BMP files must be 24 bits per pixel.

    Args:
        filename: The name of the BMP file to read.

    Returns:
        A list of lists of RGB tuples representing the pixel data.
    """
    print(f"Reading texture file {filename}...")
    pixels = []

    with open(filename, "rb") as image:
        image.seek(10)
        headerSize = struct.unpack('=l', image.read(4))[0]

        image.seek(18)
        width = struct.unpack('=l', image.read(4))[0]
        height = struct.unpack('=l', image.read(4))[0]

        image.seek(headerSize)

        for y in range(height):
            pixelRow = []

            for x in range(width):
                b = ord(image.read(1)) / 255
                g = ord(image.read(1)) / 255
                r = ord(image.read(1)) / 255
                pixelRow.append([r, g, b])

            pixels.append(pixelRow)

    return pixels, width, height


def obj_model(filename):
    """Read an OBJ file and return the vertex, texture coordinate, normal, and face data.

    Args:
        filename: The name of the OBJ file to read.

    Returns:
        A tuple containing the vertex, texture coordinate, normal, and face data.
    """

    with open(filename, 'r') as file:
        lines = file.read().splitlines()

    vertices = []
    tex_coords = []
    normals = []
    faces = []

    for line in lines:
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
            vertices.append(list(map(float, value.split(' '))))
        elif prefix == 'vt':  # texture coordinates
            # convert the string to float, each element of the list
            tex_coords.append(list(map(float, value.split(' '))))
        elif prefix == 'vn':  # normals
            # convert the string to float, each element of the list
            normals.append(list(map(float, value.split(' '))))
        elif prefix == 'f':  # faces
            facesAppend = [list(map(int, vert.split('/')))
                           for vert in value.split(' ')]
            faces.append(facesAppend)

    return vertices, tex_coords, normals, faces
