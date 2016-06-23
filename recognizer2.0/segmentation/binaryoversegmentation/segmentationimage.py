import copy

import numpy as np

from utils.image import Image


class SegmentationImage(Image):
    """An image that is being segmented"""

    def __new__(cls, image, segmentation_lines, validators=[]):
        obj = Image.__new__(cls, image, image.color_mode)
        obj._segmentation_lines = segmentation_lines
        obj._validators = validators
        return obj

    def segment(self):
        splitting_line = self._segmentation_lines.middle_segmentation_line
        return self._split_along(splitting_line)

    def _split_along(self, line):
        left = None
        right = None
        raise NotImplementedError
        # left and right are segmentation images
        return (left, right)

    @property
    def is_valid_character_image(self):
        all([validator.is_valid(self) for validator in self._validators])

    @property
    def has_segmentation_lines(self):
        return bool(self._segmentation_lines)

    @property
    def width_over_height_ratio(self):
        return self.width / self.height

    @property
    def segment_further(self):
        raise NotImplementedError()
        # width < MinimumCharacterWidth + AverageCharacterWidth
        # Still has some SSP's left

    def show(self, wait_key=None, window_name=None, **kwargs):
        if not wait_key and not wait_key == 0:
            wait_key = super(SegmentationImage, self)._default_wait_key
        image_with_ssp = copy.copy(self)
        image_with_ssp = self._segmentation_lines.paint_on(image_with_ssp, **kwargs)
        image_with_ssp.show(wait_key=wait_key, window_name=window_name)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class _AbstractSegmentationImageValidator(object):

    def __init__(self):
        super(_AbstractSegmentationImageValidator, self).__init__()

    def is_valid(self, image):
        pass

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class ValidateOnWidth(_AbstractSegmentationImageValidator):
    def __init__(self, minimum_character_width):
        _AbstractSegmentationImageValidator.__init__(self)
        self._minimum_character_width = minimum_character_width

    def is_valid(self, image):
        return image.width > self._minimum_character_width


class ValidateOnForegroundPixels(_AbstractSegmentationImageValidator):
    def __init__(self, minimum_num_foreground_pixels):
        _AbstractSegmentationImageValidator.__init__(self)
        self._minimum_num_foreground_pixels = minimum_num_foreground_pixels

    def is_valid(self, image):
        return image.number_of_foreground_pixels> self._minimum_num_foreground_pixels