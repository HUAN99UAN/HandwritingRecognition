from scipy.stats import norm

from utils.mixins import CommonEqualityMixin
import segmentation.binaryoversegmentation as config


class _AbstractCharacterValidator(CommonEqualityMixin):

    def __init__(self):
        super(_AbstractCharacterValidator, self).__init__()

    def probability(self, image):
        pass

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class ValidateOnWidth(_AbstractCharacterValidator):
    def __init__(self):
        _AbstractCharacterValidator.__init__(self)
        self._cdf = lambda x: norm.cdf(x,
                                       loc=config.character_width_distribution.mean,
                                       scale=config.character_width_distribution.sd)

    def probability(self, image):
        return 1 - self._cdf(image.width)


class ValidateOnHeight(_AbstractCharacterValidator):
    def __init__(self):
        super(ValidateOnHeight, self).__init__()
        self._cdf = lambda x: norm.cdf(x,
                                       loc=config.character_height_distribution.mean,
                                       scale=config.character_height_distribution.sd)

    def probability(self, image):
        return 1 - self._cdf(image.height)


class ValidateOnForegroundPixels(_AbstractCharacterValidator):
    def __init__(self):
        _AbstractCharacterValidator.__init__(self)
        self._cdf = lambda x: norm.cdf(x,
                                       loc=config.pixel_distribution.mean,
                                       scale=config.pixel_distribution.sd)

    def probability(self, image):
        return 1 - self._cdf(image.number_of_foreground_pixels)
