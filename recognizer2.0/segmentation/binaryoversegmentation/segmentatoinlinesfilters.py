import copy

import cv2
import numpy as np

from preprocessing.invert import Invert
from utils.image import Image, ColorMode

class _AbstractSegmentationLineFilter(object):
    """Abstract class to define the interface of segmentation line filters, for use with the build-in filter()."""

    def __init__(self, image):
        super(_AbstractSegmentationLineFilter, self).__init__()
        self.image = image

    def keep(self, segmentation_line):
        raise NotImplementedError()

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

class HoleFilter(object):
    """Return false for the segmentation lines that lie in a hole."""

    def __init__(self, image):
        super(HoleFilter, self).__init__()
        self.image = image
        # Has true at the columns where the image has a hole
        self._hole_bits = self._find_holes()

    def _find_holes(self):
        contour_image = self._compute_contour_image()
        return np.sum(contour_image, axis=0) < contour_image.height

    def _compute_contour_image(self):
        image = Invert().apply(copy.deepcopy(self.image))
        contours, hierarchy = cv2.findContours(image=image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
        contour_image = Image(np.ones(self.image.shape), color_mode=ColorMode.binary)
        cv2.drawContours(contour_image, contours=contours, contourIdx=6, color=(0, 0, 0), thickness=-1)
        contour_image.show(wait_key=0)
        return contour_image

    def keep(self, segmentation_line):
        raise NotImplementedError()

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

