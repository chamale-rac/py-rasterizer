import struct


class Texture(object):  # just for bmp files
    def __init__(self, path):
        with open(path, 'rb') as image:
            image.seek(10)
            headerSize = struct.unpack('=l', image.read(4))[0]

            image.seek(18)
            self.width = struct.unpack('=l', image.read(4))[0]
            self.height = struct.unpack('=l', image.read(4))[0]

            # assuming 24 bits or 3 bytes per pixel
            # TODO create own png to bmp converter to avoid this
            image.seek(headerSize)

            self.pixels = []
            for y in range(self.height):
                pixelRow = []

                for x in range(self.width):
                    b = ord(image.read(1)) / 255
                    g = ord(image.read(1)) / 255
                    r = ord(image.read(1)) / 255
                    pixelRow.append([r, g, b])

                self.pixels.append(pixelRow)

    def getColor(self, u, v):
        if (0 <= u < 1) and (0 <= v < 1):
            x = int(u * self.width)
            y = int(v * self.height)
            return self.pixels[y][x]
        else:
            return None
