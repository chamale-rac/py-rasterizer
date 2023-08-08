import struct


def char(c):
    """Convert a character to a byte."""
    return struct.pack("=c", c.encode("ascii"))


def word(w):
    """Convert a 16-bit integer to two bytes."""
    return struct.pack("=h", w)


def dword(d):
    """Convert a 32-bit integer to four bytes."""
    return struct.pack("=l", d)


def color(r, g, b):
    """Convert RGB values to a color byte."""
    return bytes([int(b * 255),
                  int(g * 255),
                  int(r * 255)])
