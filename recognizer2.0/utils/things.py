from collections import namedtuple
import math


_RangeTuple = namedtuple('Range', ['min', 'max'], verbose=True)
_SizeTuple = namedtuple('Size', ['width', 'height'], verbose=True)
_Pixel = namedtuple('Pixel', ['row', 'column'])
Point = namedtuple('Point', ['x', 'y'])


class Pixel(_Pixel):

    def manhattan_distance_to(self, other):
        return abs((self.row - other.row)) + abs((self.column - other.column))

    @property
    def x(self):
        return self.column

    @property
    def y(self):
        return self.row

    @property
    def move_left(self):
        return Pixel(row=self.row, column=self.column - 1)

    @property
    def move_right(self):
        return Pixel(row=self.row, column=self.column + 1)

    @property
    def move_up(self):
        return Pixel(row=self.row - 1, column=self.column)

    @property
    def move_down(self):
        return Pixel(row=self.row + 1, column=self.column)

    def is_background_in(self, image, background_color=255):
        return bool(image.get_pixel(self) == background_color)

    def neighbours_in(self, image):
        if image.get_pixel(self.move_left) is not None:
            yield self.move_left
        if image.get_pixel(self.move_right) is not None:
            yield self.move_right
        if image.get_pixel(self.move_up) is not None:
            yield self.move_up
        if image.get_pixel(self.move_down) is not None:
            yield self.move_down

    def is_on(self, line):
        return self.x == line.x

    def paint_on(self, image, color=(0, 0, 0)):
        raise NotImplementedError()
        return image


class Range(_RangeTuple):
    @property
    def length(self):
        return self.max - self.min


class Size(_SizeTuple):
    def __add__(self, other):
        try:
            width = self.width + other.width
            height = self.height + other.height
        except TypeError:
            width = self.width + other
            height = self.height + other
        return Size(width=width, height=height)

    def __radd__(self, other):
        try:
            width = self.width + other.width
            height = self.height + other.height
        except TypeError:
            width = self.width + other
            height = self.height + other
        return Size(width=width, height=height)

    def __sub__(self, other):
        try:
            width = self.width - other.width
            height = self.height - other.height
        except TypeError:
            width = self.width - other
            height = self.height - other
        return Size(width=width, height=height)

    def __rsub__(self, other):
        raise NotImplementedError("Subtracting a Size from anything other than a Size is not supported.")

    def __mul__(self, other):
        return Size(
            width=self.width * other,
            height=self.height * other
        )

    def __rmul__(self, other):
        return Size(
            width=self.width * other,
            height=self.height * other
        )

    def __div__(self, other):
        return Size(
            width=self.width/other,
            height=self.height/other
        )

    def __rdiv__(self, other):
        raise NotImplementedError("Dividing a float through a Size is not supported.")

    def __truediv__(self, other):
        return Size(
            width=self.width/float(other),
            height=self.height/float(other)
        )

    def __rtruediv__(self, other):
        raise NotImplementedError("Dividing a float through a Size is not supported.")


class PixelPath(object):

    def __init__(self, pixels):
        self._pixels = pixels

    def paint_on(self, image, color=(0, 0, 0)):
        for pixel in self._pixels:
            image = pixel.paint_on(image, color)
        return image

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

