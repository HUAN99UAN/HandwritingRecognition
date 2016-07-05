import cv2
import numpy as np

import preprocessing.colorspaces
from utils.things import Point


class Shape(object):
    def paint_on(self, image, **kwargs):
        pass

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Line(Shape):
    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2

    @property
    def p1(self):
        return self._p1

    @property
    def p2(self):
        return self._p2

    @property
    def x1(self):
        return self._p1.x

    @property
    def x2(self):
        return self._p2.x

    @property
    def y1(self):
        return self._p1.y

    @property
    def y2(self):
        return self._p2.y

    def paint_on(self, image, color=(0, 0, 0), width=10, **kwargs):
        # if not image.color_mode.is_color:
        #     image = preprocessing.colorspaces.ToColor().apply(image)
        cv2.line(image, self.p1, self.p2, color=color, thickness=width)
        return image


class VerticalLine(Line):
    def __init__(self, x, y1, y2):
        super(VerticalLine, self).__init__(Point(x, y1), Point(x, y2))

    def x(self):
        return self.p_1.x


class HorizontalLine(Line):
    def __init__(self, x1, x2, y):
        super(HorizontalLine, self).__init__(Point(x1, y), Point(x2, y))

    @property
    def left(self):
        return min(self.x1, self.x2)

    @property
    def right(self):
        return max(self.x1, self.x2)

    @property
    def y(self):
        return self._p1.y

    @property
    def width(self):
        return abs(self.x1 - self.x2)

    def distance_to(self, other):
        return abs(self.y - other.y)


class Rectangle(Shape):
    def __init__(self, corner, opposite_corner):
        _top = min(corner.y, opposite_corner.y)
        _bottom = max(corner.y, opposite_corner.y)

        _left = min(corner.x, opposite_corner.x)
        _right = max(corner.x, opposite_corner.x)

        self._top_left = Point(x=_left, y=_top)
        self._bottom_right = Point(x=_right, y=_bottom)

    @property
    def left(self):
        return self._top_left.x

    @property
    def right(self):
        return self._bottom_right.x

    @property
    def bottom(self):
        return self._bottom_right.y

    @property
    def top(self):
        return self._top_left.y

    @property
    def top_left(self):
        return self._top_left

    @property
    def top_right(self):
        return Point(x=self.right, y=self.top)

    @property
    def bottom_left(self):
        return Point(x=self.left, y=self.bottom)

    @property
    def bottom_right(self):
        return self._bottom_right

    @property
    def width(self):
        return abs(self.right - self.left)

    @property
    def height(self):
        return abs(self.bottom - self.top)

    def paint_on(self, image, color=(0, 0, 0), width=10, filled=False, **kwargs):
        if not image.color_mode.is_color:
            image = preprocessing.colorspaces.ToColor().apply(image)
        if filled:
            width = -1
        cv2.rectangle(image, self.top_left, self.bottom_right, color=color, thickness=width)
        return image
