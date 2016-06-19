from collections import namedtuple


_RangeTuple = namedtuple('Range', ['min', 'max'], verbose=True)
_SizeTuple = namedtuple('Size', ['width', 'height'], verbose=True)


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

