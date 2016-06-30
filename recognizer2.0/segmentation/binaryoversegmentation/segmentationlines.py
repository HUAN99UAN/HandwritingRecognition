import numpy as np

from utils.shapes import VerticalLine
from utils.mixins import CommonEqualityMixin


class SegmentationLines(object):
    """Object to collect segmentation lines, basically a wrapper around a list."""

    def __init__(self, lines):
        super(SegmentationLines, self).__init__()
        self._lines = lines
        self._idx = 0

    @property
    def is_empty(self):
        return not bool(self._lines)

    def lines(self):
        for line in self._lines:
            yield line

    def paint_on(self, image, color=(0, 0, 0), width=1):
        for line in self._lines:
            image = line.paint_on(image, color=color, width=width)
        return image

    def get_subset_in(self, bounding_box):
        new_set = filter(
            lambda line: line.x in range(bounding_box.left, bounding_box.right + 1),
            self._lines)
        return SegmentationLines(new_set)

    def __iter__(self):
        self._idx = 0
        return self

    def next(self):
        if self._idx < len(self._lines):
            self._idx += 1
            return self._lines[self._idx - 1]
        else:
            raise StopIteration

    def filter(self, filter_method):
        new_lines = filter(filter_method, self._lines)
        return SegmentationLines(lines=new_lines)

    def line_closest_to(self, value):
        idx = np.argmin(abs(self.coordinates - value))
        return self._lines[idx]

    def line_at_idx(self, idx):
        return self._lines[idx]

    @property
    def coordinates(self):
        return np.array([line.x for line in self._lines])

    @staticmethod
    def from_x_coordinates(x_coordinates):
        lines = list()
        for x in x_coordinates:
            lines.append(SegmentationLine(x=x))
        return SegmentationLines(lines)

    @staticmethod
    def from_suspicious_regions(regions, stroke_width):
        lines = list()
        for region in regions:
            lines.extend(region.to_segmentation_lines())
        return SegmentationLines(lines)

    def shift_horizontally(self, distance_to_shift):
        new_lines = [line.shift_horizontally(distance_to_shift) for line in self._lines]
        return SegmentationLines(lines=new_lines)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._lines == other._lines

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<SegmentationLines lines: {lines}>".format(lines=self._lines)


class SegmentationLine(CommonEqualityMixin):
    def __init__(self, x):
        self._x = x

    def shift_horizontally(self, distance_to_shift):
        return SegmentationLine(x=self._x + distance_to_shift)

    def distance_to(self, other_x):
        return abs(self._x - other_x)

    @property
    def x(self):
        return self._x

    def paint_on(self, image, color=(0,0,0), width=1, top=None, bottom=None):
        top = top or 0
        bottom = bottom or image.height
        return VerticalLine(
            x=self.x, y1=top, y2=bottom
        ).paint_on(image, color=color, width=width)

    def __repr__(self):
        return "SegmentationLine x: {x}>".format(x=self.x)