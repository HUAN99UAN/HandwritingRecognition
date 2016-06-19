from collections import namedtuple


Range = namedtuple('Range', ['min', 'max'], verbose=True)


SizeTuple = namedtuple('Size', ['width', 'height'], verbose=True)


class Size(SizeTuple):
    def __add__(self, other):
        return Size(
            width=self.width + other.width,
            height=self.height + other.height
        )

    def __sub__(self, other):
        return Size(
            width=self.width - other.width,
            height=self.height - other.height
        )

    def __mul__(self, other):
        return Size(
            width=self.width * other.width,
            height=self.height * other.height
        )

    def __div__(self, other):
        return Size(
            width=self.width / other.width,
            height=self.height / other.height
        )