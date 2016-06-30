import cv2

import utils.image
import interface
import colorspaces


class OtsuMethod(interface.AbstractFilter):
    """Implementation of Otsu's Method for thresholding."""

    def __init__(self, maximum_value=255):
        super(OtsuMethod, self).__init__()
        self._maximum_value = maximum_value

    @classmethod
    def _verify_image(cls, image):
        if not image.color_mode.is_gray:
            image = colorspaces.ToGrayScale().apply(image)
        return image

    def apply(self, image):
        image = self._verify_image(image)
        _, otsu_image = cv2.threshold(
            image, thresh=0, maxval=self._maximum_value, type=cv2.THRESH_OTSU+cv2.THRESH_BINARY
        )
        return utils.image.Image(otsu_image, color_mode=utils.image.ColorMode.binary)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
