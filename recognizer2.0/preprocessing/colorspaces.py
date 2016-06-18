import warnings

import cv2

import interface
from utils.image import Image, ColorMode


class ToGrayScale(interface.AbstractFilter):
    """Convert a B G R image to gray scale."""

    def __init__(self):
        super(ToGrayScale, self).__init__()

    def apply(self, image):
        if image.is_gray_scale:
            warnings.warn('The image seems to be gray scale, thus it is not converted, but returned as is.')
            return image
        return Image(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), color_mode=ColorMode.gray)


class ToColor(interface.AbstractFilter):
    """Convert a gray scale image to an image in the B G R space."""

    def __init__(self):
        super(ToColor, self).__init__()

    def apply(self, image):
        if not image.is_gray_scale:
            warnings.warn('The image seems not to be gray scale, thus it is not converted, but returned as is.')
            return image
        return Image(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR), color_mode=ColorMode.bgr)


if __name__ == '__main__':
    image_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/input.ppm'
    image = Image.from_file(image_file)
    gray_image = ToGrayScale().apply(image)
    gray_image.show('Gray Scale')
    color_image = ToColor().apply(gray_image)
    color_image.show('Color Scale, but still BW')
