import interface
from utils.image import WrongColorModeError


class Invert(interface.AbstractFilter):
    """Invert the colors in the image."""

    def __init__(self):
        super(Invert, self).__init__()

    def apply(self, image):
        if image.color_mode.is_color:
            raise WrongColorModeError("This operation is not supported for color images.")
        return 255 - image

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

