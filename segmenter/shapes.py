from typing import Sequence

import PIL

from utils import Point, IntFloat


class Shape:
    def paint_on(self, image):
        pass

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Rectangle(Shape):
    def __init__(self, top_left, bottom_right):
        self._top_left = top_left
        self._bottom_right = bottom_right

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
        return self.right - self.left
    
    @property
    def height(self):
        return self.top - self.bottom

    @property
    def points(self):
        return [
            self.top_left,
            self.top_right,
            self.bottom_right,
            self.bottom_left
        ]

    def _pil_points(self):
        return [self.top_left, self.bottom_right]

    def paint_on(self, image):
        painter = PIL.ImageDraw.Draw(image)
        # Cannot get the colors to work, so we'll just live with grey for now.
        painter.rectangle(self._pil_points(), fill=None, outline=None)
        del painter
