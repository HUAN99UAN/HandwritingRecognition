from utils.shapes import VerticalLine

import numpy as np


class SegmentationLines(object):
    """Object to collect segmentation lines, basically a wrapper around a list."""

    def __init__(self, lines):
        super(SegmentationLines, self).__init__()
        self._lines= lines

    def lines(self):
        for line in self._lines:
            yield line

    def paint_on(self, image, color=(0, 0, 0), width=10):
        for line in self._lines:
            image = line.paint_on(image, color=color, width=width)
        return image

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