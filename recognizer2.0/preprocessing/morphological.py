import warnings

import cv2

import interface
from utils.image import Image
from colorspaces import ToGrayScale


class _MorphologicalFilter(interface.AbstractFilter):

    def __init__(self, mask, iterations):
        super(_MorphologicalFilter, self).__init__()
        self._mask = mask
        self._iterations = iterations

    @classmethod
    def fix_image_color_mode(cls, image):
        if not image.color_mode.is_gray:
            warnings.warn('Morphological operations are only supported on gray scale images, converting '
                          'the image to gray scale before applying the operation.')
            image = ToGrayScale().apply(image)
        return image

    @classmethod
    def _apply_until_stability(self, image, operation):
        new_image = operation.apply(image)
        while new_image is not image:
            image, new_image = new_image, operation.apply(new_image)
        return image


class Erosion(_MorphologicalFilter):
    _default_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, mask=None, iterations=1):
        super(Erosion, self).__init__(
            mask=mask or self.__class__._default_mask,
            iterations=iterations)

    def apply(self, image):
        image = self.fix_image_color_mode(image)
        return Image(cv2.erode(image, self._mask, iterations=self._iterations), color_mode=image.color_mode)


class Dilation(_MorphologicalFilter):
    _default_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, mask=None, iterations=1):
        super(Dilation, self).__init__(
            mask=mask or self.__class__._default_mask,
            iterations=iterations)

    def apply(self, image):
        image = self.fix_image_color_mode(image)
        return Image(cv2.dilate(image, self._mask, iterations=self._iterations), color_mode=image.color_mode)


class Opening(_MorphologicalFilter):
    _default_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, mask=None, iterations=1):
        super(Opening, self).__init__(
            mask=mask or self.__class__._default_mask,
            iterations=iterations)

    def apply(self, image):
        image = self.fix_image_color_mode(image)
        return Image(
            cv2.morphologyEx(image, cv2.MORPH_OPEN, self.mask, iterations=self._iterations),
            color_mode=image.color_mode
        )


class Closing(_MorphologicalFilter):
    _default_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, mask=None, iterations=1):
        super(Closing, self).__init__(
            mask=mask or self.__class__._default_mask,
            iterations=iterations)

    def apply(self, image):
        image = self.fix_image_color_mode(image)
        return Image(
            cv2.morphologyEx(image, cv2.MORPH_CLOSE, self.mask, iterations=self._iterations),
            color_mode=image.color_mode
        )


class ReconstructionByErosion(_MorphologicalFilter):
    _default_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, mask=None):
        super(ReconstructionByErosion, self).__init__(
            mask=mask or self.__class__._default_mask,
            iterations=1)

    def apply(self, image):
        erosion = Erosion(mask=self._mask, iterations=1)
        self._apply_until_stability(image, erosion)


class ReconstructionByDilation(_MorphologicalFilter):
    _default_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def apply(self, image):
        dilation = Dilation(mask=self._mask, iterations=1)
        self._apply_until_stability(image, dilation)


class ReconstructionByOpening(_MorphologicalFilter):
    _default_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, mask, size=1):
        super(ReconstructionByOpening, self).__init__(
            mask=mask or self._default_mask,
            iterations=size
        )

    def apply(self, image):
        image = self.fix_image_color_mode(image)
        eroded_image = Erosion(mask=self._mask, iterations=self._iterations).apply(image)
        return ReconstructionByDilation(mask=self._mask).apply(eroded_image)


class ReconstructionByClosing(_MorphologicalFilter):
    _default_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, mask, size=1):
        super(ReconstructionByClosing, self).__init__(
            mask=mask or self._default_mask,
            iterations=size
        )

    def apply(self, image):
        image = self.fix_image_color_mode(image)
        eroded_image = Dilation(mask=self._mask, iterations=self._iterations).apply(image)
        return ReconstructionByErosion(mask=self._mask).apply(eroded_image)

if __name__ == '__main__':
    # image_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/input.ppm'
    image_file = '/Users/laura/Desktop/opening_1.png'
    image = Image.from_file(image_file)
    image.show(wait_key=0)
    new_image = Dilation().apply(image)
    new_image.show(wait_key=0)