import warnings

import cv2

import interface
from utils.image import Image, ColorMode


class ToGrayScale(interface.AbstractFilter):
    """Convert a B G R image to gray scale."""

    def __init__(self):
        super(ToGrayScale, self).__init__()

    def apply(self, image):
        cv2_transformation_key = cv2.COLOR_BGR2GRAY
        if image.color_mode.is_gray:
            warnings.warn('The image is already in gray scale, it is returned as is.')
            return image
        if image.color_mode.is_binary:
            cv2_transformation_key = cv2.COLOR_GRAY2BGR
        return Image(cv2.cvtColor(image, cv2_transformation_key), color_mode=ColorMode.gray)


class ToColor(interface.AbstractFilter):
    """Convert a gray scale image to an image in the B G R space."""

    def __init__(self):
        super(ToColor, self).__init__()

    def apply(self, image):
        if image.color_mode.is_color:
            warnings.warn('The image is already in colormode, it is returned as is.')
            return image
        return Image(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR), color_mode=ColorMode.bgr)


class ToBinary(interface.AbstractFilter):
    """Convert an image to binary."""

    def __init__(self, threshold=128):
        super(ToBinary, self).__init__()
        self._threshold = threshold

    def apply(self, image):
        if image.color_mode.is_binary:
            warnings.warn('The image is already in binary, it is returned as is.')
            return image
        if image.color_mode.is_color:
            image = ToGrayScale().apply(image)
        _, binary_image_array = cv2.threshold(image, self._threshold, 255, cv2.THRESH_BINARY)
        return Image(binary_image_array, color_mode=ColorMode.binary)

