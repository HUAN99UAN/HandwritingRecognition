import copy

import cv2
import numpy as np

from preprocessing.invert import Invert
from utils.image import Image, ColorMode
from utils.mixins import CommonEqualityMixin


class _AbstractSegmentationLineFilter(CommonEqualityMixin):
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
        try:
            contour_image = self._compute_contour_image()
            return np.sum(contour_image, axis=0) < contour_image.height
        except TypeError:
            # cv2.findContours returns None, no holes, we assume, return a list of falses.
            return np.zeros(self.image.shape[1], dtype=np.bool)

    def _compute_contour_image(self):
        try:
            image = Invert().apply(copy.deepcopy(self.image))
            contours, hierarchy = cv2.findContours(image=image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
            inner_contours = self._find_inner_contours(hierarchy)
            contour_image = self._add_contours_to_image(contours, inner_contours)
            return contour_image
        except TypeError:
            raise

    def _find_inner_contours(self, hierarchy):
        inner_contours = list()
        try:
            for contour, idx in zip(hierarchy[0], range(len(hierarchy[0]))):
                if contour[3] != -1:
                    inner_contours.append(idx)
            return inner_contours
        except TypeError:
            raise

    def _add_contours_to_image(self, contours, contour_idx, contour_image=None):
        if not contour_image:
            contour_image = Image(np.ones(self.image.shape), color_mode=ColorMode.binary)
        for idx in contour_idx:
            cv2.drawContours(contour_image, contours=contours, contourIdx=idx, color=(0, 0, 0), thickness=-1)
        return contour_image

    def keep(self, segmentation_line):
        return not self._hole_bits[segmentation_line.x]

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

