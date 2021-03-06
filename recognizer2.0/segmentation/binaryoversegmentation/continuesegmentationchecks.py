from utils.mixins import CommonEqualityMixin
import segmentation.binaryoversegmentation as config

class _AbstractContinueSegmentationCheck(CommonEqualityMixin):

    def __init__(self):
        super(_AbstractContinueSegmentationCheck, self).__init__()

    def continue_segmentation(self, image):
        pass

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class ContinueOnWidthCheck(_AbstractContinueSegmentationCheck):
    """
    Segment the image further if its width is greater than minimum_character_width + average_character_width.
    """
    def __init__(self):
        super(ContinueOnWidthCheck, self).__init__()
        self._maximum_image_width = config.default_maximum_character_size.width
        self._minimum_image_width = config.default_minimum_character_size.width

    def continue_segmentation(self, image):
        return image.width >= 2 * self._minimum_image_width


class ContinueOnSSPCheck(_AbstractContinueSegmentationCheck):
    """
    Segment the image further if it has SSP left.
    """
    def __init__(self):
        super(ContinueOnSSPCheck, self).__init__()

    def continue_segmentation(self, image):
        return image.has_segmentation_lines


class ContinueOnNumberOfForegroundPixels(_AbstractContinueSegmentationCheck):

    def __init__(self):
        self._minimum_number_of_foreground_pixels = config.default_num_foreground_pixels.min

    def continue_segmentation(self, image):
        return image.number_of_foreground_pixels >= self._minimum_number_of_foreground_pixels
