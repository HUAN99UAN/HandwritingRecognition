import warnings

import numpy as np

from preprocessing.colorspaces import ToBinary
from preprocessing.invert import Invert
from utils.shapes import Rectangle
from utils.things import Point


class SuspiciousRegionsComputer:
    """docstring for ClassName"""

    def __init__(self, threshold):
        self._threshold = threshold

    @classmethod
    def _binarize_image(cls, image):
        if not image.color_mode.binary:
            warnings.warn('Expected a binary image, the image is converted to binary with a default threshold.')
        return ToBinary(maximum_value=1).apply(image)

    def compute(self, image):
        frequencies = self._vertical_pixel_densities(image)
        return self._to_suspicious_regions(frequencies=frequencies, image_height=image.height)

    def _vertical_pixel_densities(self, image):
        image = Invert().apply(self._binarize_image(image))
        frequencies = np.sum(image, axis=0)
        return frequencies

    def _to_suspicious_regions(self, frequencies, image_height):
        sequences_of_suspicious_segmentation_lines = self._to_sequences(frequencies)
        return [
            SuspiciousRegion(x0=x0, x1=x1, image_height=image_height)
            for (x0, x1)
            in sequences_of_suspicious_segmentation_lines
        ]

    def _to_sequences(self, frequencies):
        bits = np.asarray(frequencies <= self._threshold, dtype=np.uint8)
        bounded = np.hstack(([0], bits, [0]))
        # get 1 at run starts and -1 at run ends
        difs = np.diff(bounded)
        run_starts, = np.where(difs > 0)
        run_ends, = np.where(difs < 0)
        return zip(run_starts, run_ends)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class SuspiciousRegion(Rectangle):

    def __init__(self, x0, x1, image_height):
        x0, x1 = min(x0, x1), max(x0, x1)
        top_left = Point(x=x0, y=0)
        bottom_right = Point(x=x1, y=image_height)
        super(SuspiciousRegion, self).__init__(top_left=top_left, bottom_right=bottom_right)

    def to_segmentation_lines(self, stroke_width):
        if self.width < stroke_width:
            return self._segmentation_line_in_center()
        if self.width >= stroke_width:
            return self._to_segmentation_lines(stroke_width)

    @classmethod
    def _segmentation_line_in_center(cls):
        raise NotImplementedError()
        # should return a list!

    @classmethod
    def _to_segmentation_lines(cls):
        raise NotImplementedError()
        # should return a list!