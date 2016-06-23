import warnings

import numpy as np

from preprocessing.colorspaces import ToBinary
from preprocessing.invert import Invert
from utils.shapes import Rectangle, HorizontalLine
from utils.things import Point
from segmentation.binaryoversegmentation.segmentationlines import SegmentationLine, SegmentationLines


class SuspiciousRegionsComputer:
    """docstring for ClassName"""

    def __init__(self, threshold):
        self._threshold = threshold

        self._image = None

    def _binarize_image(self):
        if not self._image.color_mode.binary:
            warnings.warn('Expected a binary image, the image is converted to binary with a default threshold.')
        return ToBinary(maximum_value=1).apply(self._image)

    def compute(self, image):
        self._image = image
        frequencies = self._vertical_pixel_densities()
        suspicious_regions =  self._to_suspicious_regions(frequencies=frequencies)
        self.clean_up()
        return suspicious_regions

    def _vertical_pixel_densities(self):
        image = Invert().apply(self._binarize_image())
        frequencies = np.sum(image, axis=0)
        return frequencies

    def _to_suspicious_regions(self, frequencies):
        sequences_of_suspicious_segmentation_lines = self._to_sequences(frequencies)
        return SuspiciousRegions([
            SuspiciousRegion(x0=x0, x1=x1, image_height=self._image.height)
            for (x0, x1)
            in sequences_of_suspicious_segmentation_lines
        ])

    def _to_sequences(self, frequencies):
        bits = np.asarray(frequencies <= self._threshold, dtype=np.uint8)
        bounded = np.hstack(([0], bits, [0]))
        # get 1 at run starts and -1 at run ends
        difs = np.diff(bounded)
        run_starts, = np.where(difs > 0)
        run_ends, = np.where(difs < 0)
        self._fix_boundary_of_last_suspicious_region(run_ends)
        return zip(run_starts, run_ends)

    def _fix_boundary_of_last_suspicious_region(self, run_ends):
        if run_ends[-1:] == self._image.width:
            run_ends[-1:] -= 1

    def clean_up(self):
        self._image = None

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class SuspiciousRegions():
    def __init__(self, regions):
        self._regions = regions

    def to_segmentation_lines(self, stroke_width):
        lines = []
        for region in self._regions:
            lines.extend(region.to_segmentation_lines(stroke_width))
        return SegmentationLines(lines)

    def paint_on(self, image, color=(0,0,0), width=10, filled=False):
        for region in self._regions:
            image = region.paint_on(image, color=color, width=width, filled=filled)
        return image


class SuspiciousRegion(HorizontalLine):

    def __init__(self, x0, x1, image_height):
        x0, x1 = min(x0, x1), max(x0, x1)
        top_left = Point(x=x0, y=0)
        bottom_right = Point(x=x1, y=image_height)
        super(SuspiciousRegion, self).__init__(x1=x0, x2=x1, y=0)

    def to_segmentation_lines(self, stroke_width):
        if self.width < stroke_width:
            return self._segmentation_line_in_center()
        if self.width >= stroke_width:
            return self._to_segmentation_lines(stroke_width)

    def _segmentation_line_in_center(self):
        x = round((self.left + self.right)/ 2.0)
        return [SegmentationLine(x=x)]

    def _to_segmentation_lines(self, stroke_width):
        segmentation_lines = []
        for x in range(self.left, self.right, stroke_width):
            segmentation_lines.append(
                SegmentationLine(x=x)
            )
        segmentation_lines.append(SegmentationLine(x=self.right))
        return segmentation_lines

    def paint_on(self, image, color=(0, 0, 0), width=10, as_rectangle=True, bottom=None, top=None, filled=True):
        if as_rectangle:
            top = top or 0
            bottom = bottom or image.height
            return Rectangle(
                top_left=Point(x=self.left, y=top),
                bottom_right=Point(x=self.right, y=bottom)
            ).paint_on(
                image=image, color=color, width=width, filled=filled
            )
        else:
            return super(SuspiciousRegion, self).paint_on(image, color, width)
