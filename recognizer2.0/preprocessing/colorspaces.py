import warnings

import cv2

import interface
from utils.image import Image


class ToGrayScale(interface.AbstractFilter):
    """Convert an B G R image to gray scale."""

    def __init__(self):
        super(ToGrayScale, self).__init__()

    @classmethod
    def is_gray_scale(cls, image):
        return len(image.shape) == 2

    def apply(self, image):
        if self.is_gray_scale(image):
            warnings.warn('The image seems to be gray scale, thus it is not converted, but returned as is.')
            return image
        return Image(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

if __name__ == '__main__':
    image_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/input.ppm'
    image = Image.from_file(image_file)
    new_image = ToGrayScale().apply(image)
    new_new_image = ToGrayScale().apply(new_image)
    new_new_image.show()
