from utils.mixins import CommonEqualityMixin
import segmentation.binaryoversegmentation as config


class _AbstractCharacterValidator(CommonEqualityMixin):

    def __init__(self):
        super(_AbstractCharacterValidator, self).__init__()

    def is_valid(self, image):
        pass

    def is_valid(self, image):
        pass

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class ValidateOnWidth(_AbstractCharacterValidator):
    def __init__(self):
        _AbstractCharacterValidator.__init__(self)
        self._minimum_character_width = config.default_minimum_character_size.width
        self._maximum_character_width = config.default_maximum_character_size.width

    def is_valid(self, image):
        return (image.width >= self._minimum_character_width) and (image.width <= self._maximum_character_width)


class ValidateOnHeight(_AbstractCharacterValidator):
    def __init__(self):
        super(ValidateOnHeight, self).__init__()
        self._minimum_character_height = config.default_minimum_character_size.height
        self._maximum_character_height = config.default_maximum_character_size.height

    def is_valid(self, image):
        return (image.height >= self._minimum_character_height) and (image.height <= self._maximum_character_height)


class ValidateOnForegroundPixels(_AbstractCharacterValidator):
    def __init__(self):
        _AbstractCharacterValidator.__init__(self)
        self._minimum_num_foreground_pixels = config.default_num_foreground_pixels.min

    def is_valid(self, image):
        return image.number_of_foreground_pixels >= self._minimum_num_foreground_pixels
