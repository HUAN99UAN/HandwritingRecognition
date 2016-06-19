import warnings

import cv2

import interface
from utils.image import Image, ColorMode


class ToGrayScale(interface.AbstractFilter):
    """Convert a B G R image to gray scale."""

    def __init__(self):
        super(ToGrayScale, self).__init__()

    def apply(self, image):
        if image.color_mode.is_gray:
            warnings.warn('The image is already in gray scale, it is returned as is.')
            return image
        return Image(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), color_mode=ColorMode.gray)


class ToColor(interface.AbstractFilter):
    """Convert a gray scale image to an image in the B G R space."""

    def __init__(self):
        super(ToColor, self).__init__()

    def apply(self, image):
        if not image.color_mode.is_bgr:
            warnings.warn('The image is already in colormode, it is returned as is.')
            return image
        return Image(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR), color_mode=ColorMode.bgr)


if __name__ == '__main__':
    image_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/input.ppm'
    image = Image.from_file(image_file)
    gray_image = ToGrayScale().apply(image)
    gray_image.show(window_name='Gray Scale')
    color_image = ToColor().apply(gray_image)
    color_image.show(window_name='Color Scale, but still BW')
