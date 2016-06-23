from utils.image import Image


class SegmentationImage(Image):
    """An image that is being segmented"""

    def __init__(self, image, segmentation_lines, validators = []):
        super(SegmentationImage, self).__init__(image, image.color_mode)
        self._segmentation_lines = segmentation_lines
        self._validators = validators

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
    def __init__(self, minimum_character_width=None):
        _AbstractSegmentationImageValidator.__init__(self)
        self._minimum_character_width = minimum_character_width
        raise NotImplementedError("What should the minimum character width be?")

    def is_valid(self, image):
        return image.width > self._minimum_character_width


class ValidateOnForegroundPixels(_AbstractSegmentationImageValidator):
    def __init__(self, minimum_num_foreground_pixels=None):
        _AbstractSegmentationImageValidator.__init__(self)
        self._minimum_num_foreground_pixels = minimum_num_foreground_pixels
        raise NotImplementedError("What should the number of foreground pixels be?")

    def is_valid(self, image):
        return image.number_of_foreground_pixels> self._minimum_num_foreground_pixels