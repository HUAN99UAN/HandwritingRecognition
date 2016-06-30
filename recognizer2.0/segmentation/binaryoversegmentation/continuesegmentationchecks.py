from scipy.stats import norm

from utils.mixins import CommonEqualityMixin
import segmentation.binaryoversegmentation as config


class _AbstractContinueSegmentationCheck(CommonEqualityMixin):

    def __init__(self):
        super(_AbstractContinueSegmentationCheck, self).__init__()

    def probability(self, image):
        pass

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class ContinueOnWidthCheck(_AbstractContinueSegmentationCheck):
    """
    Segment the image further if its width is greater than minimum_character_width + average_character_width.
    """
    def __init__(self):
        super(ContinueOnWidthCheck, self).__init__()
        self._cdf = lambda x: norm.cdf(x,
                                       loc=config.character_width_distribution.mean,
                                       scale=config.character_width_distribution.sd)

    def probability(self, image):
        return 1 - self._cdf(image.width)


class ContinueOnHeightCheck(_AbstractContinueSegmentationCheck):
    """
    Segment the image further if its width is greater than minimum_character_width + average_character_width.
    """
    def __init__(self):
        super(ContinueOnHeightCheck, self).__init__()
        self._cdf = lambda x: norm.cdf(x,
                                       loc=config.character_height_distribution.mean,
                                       scale=config.character_height_distribution.sd)

    def probability(self, image):
        return 1 - self._cdf(image.height)

class ContinueOnSSPCheck(_AbstractContinueSegmentationCheck):
    """
    Segment the image further if it has SSP left.
    """
    def __init__(self):
        super(ContinueOnSSPCheck, self).__init__()

    def probability(self, image):
        return int(image.has_segmentation_lines)


class ContinueOnNumberOfForegroundPixels(_AbstractContinueSegmentationCheck):

    def __init__(self):
        super(ContinueOnNumberOfForegroundPixels, self).__init__()
        self._cdf = lambda x: norm.cdf(x,
                                       loc=config.pixel_distribution.mean,
                                       scale=config.pixel_distribution.sd)

    def probability(self, image):
        return 1 - self._cdf(image.width)
