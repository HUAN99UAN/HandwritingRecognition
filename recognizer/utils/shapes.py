from PIL import ImageDraw

from utils.point import Point


class Shape:
    def paint_on(self, image):
        pass

    def pil_points(self):
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

    def _pil_points(self):
        return [self.p1, self.p2]

    def paint_on(self, image):
        painter = ImageDraw.Draw(image)
        # Cannot get the colors to work, so we'll just live with grey for now.
        painter.line(self._pil_points(), fill=0, width=1)
        del painter


class HorizontalLine(Line):

    def __init__(self, x1, x2, y):
        super(HorizontalLine, self).__init__(Point(x1, y), Point(x2, y))

    @property
    def y(self):
        return self._p1.y

    def distance_to(self, other):
        return abs(self.y - other.y)


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
        return abs(self.right - self.left)
    
    @property
    def height(self):
        return abs(self.bottom - self.top)

    def _pil_points(self):
        return [self.top_left, self.bottom_right]

    def paint_on(self, image):
        painter = ImageDraw.Draw(image)
        # Cannot get the colors to work, so we'll just live with grey for now.
        painter.rectangle(self._pil_points(), fill=None, outline=None)
        del painter
