from typing import Sequence

import PIL

from utils import Point, Color, IntFloat


class Shape:
    def paint_on(self, image:PIL.Image) -> None:
        pass

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Rectangle(Shape):
    def __init__(self, top_left: Point, bottom_right: Point) -> 'Rectangle':
        self._top_left = top_left
        self._bottom_right = bottom_right

    @property
    def left(self) -> IntFloat:
        return self._top_left.x

    @property
    def right(self) -> IntFloat:
        return self._bottom_right.x

    @property
    def bottom(self) -> IntFloat:
        return self._bottom_right.y

    @property
    def top(self) -> IntFloat:
        return self._top_left.y

    @property
    def top_left(self) -> Point:
        return self._top_left

    @property
    def top_right(self) -> Point:
        return Point(x=self.right, y=self.top)

    @property
    def bottom_left(self) -> Point:
        return Point(x=self.left, y=self.bottom)

    @property
    def bottom_right(self) -> Point:
        return self._bottom_right

    @property
    def points(self) -> Sequence[Point]:
        return [
            self.top_left,
            self.top_right,
            self.bottom_right,
            self.bottom_left
        ]

    def _pil_points(self):
        return [self.top_left, self.bottom_right]

    def paint(self, image : PIL.Image) -> None:
        painter = PIL.ImageDraw.Draw(image)
        # Cannot control the color of the image, no matter what I do.
        painter.rectangle(
            rectangle=self._pil_points(),
            fill=None, outline=None
        )
        del painter
