from utils.shapes import VerticalLine

import numpy as np


class SegmentationLines(object):
    """Object to collect segmentation lines, basically a wrapper around a list."""

    def __init__(self, lines):
        super(SegmentationLines, self).__init__()
        self._lines= lines
        self._idx = 0

    def lines(self):
        for line in self._lines:
            yield line

    def paint_on(self, image, color=(0, 0, 0), width=1):
        for line in self._lines:
            image = line.paint_on(image, color=color, width=width)
        return image

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

    @property
    def middle_segmentation_line(self):
        raise NotImplementedError()

    @staticmethod
    def from_x_coordinates(x_coordinates, image_height):
        lines = list()
        for x in np.nditer(x_coordinates):
            lines.append(VerticalLine(x=x, y1=0, y2=image_height))
        return SegmentationLines(lines)

    @staticmethod
    def from_suspicious_regions(regions, stroke_width):
        lines = list()
        for region in regions:
            lines.extend(region.to_segmentation_lines())
        return SegmentationLines(lines)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class SegmentationLine():
    def __init__(self, x):
        self._x = x

    @property
    def x(self):
        return self._x

    def paint_on(self, image, color=(0,0,0), width=1, top=None, bottom=None):
        top = top or 0
        bottom = bottom or image.height
        return VerticalLine(
            x=self.x, y1=top, y2=bottom
        ).paint_on(image, color=color, width=width)