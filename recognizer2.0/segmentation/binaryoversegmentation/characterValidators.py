class _AbstractCharacterValidator(object):

    def __init__(self):
        super(_AbstractCharacterValidator, self).__init__()

    def is_valid(self, image):
        pass

    def is_valid(self, image):
        pass

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class ValidateOnWidth(_AbstractCharacterValidator):
    def __init__(self, minimum_character_width):
        _AbstractCharacterValidator.__init__(self)
        self._minimum_character_width = minimum_character_width

    def is_valid(self, image):
        return image.width > self._minimum_character_width


class ValidateOnForegroundPixels(_AbstractCharacterValidator):
    def __init__(self, minimum_num_foreground_pixels):
        _AbstractCharacterValidator.__init__(self)
        self._minimum_num_foreground_pixels = minimum_num_foreground_pixels

    def is_valid(self, image):
        return image.number_of_foreground_pixels> self._minimum_num_foreground_pixels
