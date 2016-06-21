import warnings

import numpy as np

import interface
from preprocessing.colorspaces import ToBinary
from preprocessing.invert import Invert
from segmentation.segmentationlines import SegmentationLines


class VerticalPixelDensity(interface.AbstractSegmenter):
    """docstring for ClassName"""

    def __init__(self, threshold):
        super(VerticalPixelDensity, self).__init__()
        self._threshold = threshold

    @classmethod
    def _binarize_image(cls, image):
        if not image.color_mode.binary:
            warnings.warn('Expected a binary image, the image is converted to binary with a default threshold.')
        return ToBinary(maximum_value=1).apply(image)

    def segment(self, image, as_images=True):
        as_lines = not as_images
        frequencies = self._vertical_pixel_densities(image)
        x_coordinates = np.where(frequencies >= self._threshold)
        if as_images:
            return self._to_images(x_coordinates)
        if as_lines:
            return SegmentationLines.from_x_coordinates(x_coordinates, image_height=image.height)

    def _vertical_pixel_densities(self, image):
        image = Invert().apply(self._binarize_image(image))
        frequencies = np.sum(image, axis=0)
        return frequencies

    @classmethod
    def _to_images(cls, x_coordinates):
        raise NotImplementedError("This option is not (yet) supported.")

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

