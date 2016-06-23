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
