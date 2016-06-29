import warnings

import cv2

import interface
import utils.image


class ToGrayScale(interface.AbstractFilter):
    """Convert a B G R image to gray scale."""

    def __init__(self):
        super(ToGrayScale, self).__init__()

    def apply(self, image):
        cv2_transformation_key = cv2.COLOR_BGR2GRAY
        if image.color_mode.is_gray:
            return image
        if image.color_mode.is_binary:
            cv2_transformation_key = cv2.COLOR_GRAY2BGR
        return utils.image.Image(cv2.cvtColor(image, cv2_transformation_key), color_mode=utils.image.ColorMode.gray)


class ToColor(interface.AbstractFilter):
    """Convert a gray scale image to an image in the B G R space."""

    def __init__(self):
        super(ToColor, self).__init__()

    def apply(self, image):
        if image.color_mode.is_color:
            return image
        return utils.image.Image(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR), color_mode=utils.image.ColorMode.bgr)


class ToBinary(interface.AbstractFilter):
    """Convert an image to binary."""

    def __init__(self, threshold=128, maximum_value=255):
        super(ToBinary, self).__init__()
        self._threshold = threshold
        self._maximum_value = maximum_value

    def apply(self, image):
        if image.color_mode.is_color:
            image = ToGrayScale().apply(image)
        _, binary_image_array = cv2.threshold(image, self._threshold, self._maximum_value, cv2.THRESH_BINARY)
        return utils.image.Image(binary_image_array, color_mode=utils.image.ColorMode.binary)

