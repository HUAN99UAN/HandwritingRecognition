import warnings

import cv2
import numpy as np

import interface
from utils.image import Image, ColorMode, WrongColorModeError
from colorspaces import ToGrayScale, ToBinary


class _MorphologicalFilter(interface.AbstractFilter):

    def __init__(self, structuring_element, iterations):
        super(_MorphologicalFilter, self).__init__()
        self._structuring_element = structuring_element
        self._iterations = iterations

    @classmethod
    def gray_scale_or_binary_check(cls, image):
        if image.color_mode not in [ColorMode.gray, ColorMode.binary]:
            raise WrongColorModeError("This operation can only be performed on binary or gray scale images.")

    @classmethod
    def binary_check(cls, image):
        if image.color_mode is not ColorMode.binary:
            raise WrongColorModeError("This operation can only be performed on binary images.")

    @classmethod
    def _apply_until_stability(self, image, operation):
        new_image = operation.apply(image)
        raise NotImplementedError("Implementatie is nog niet 100% correct.")
        # while new_image is not image:
        #     image, new_image = new_image, operation.apply(new_image)
        # return image


class Erosion(_MorphologicalFilter):
    _default_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, structuring_element=_default_mask, iterations=1):
        super(Erosion, self).__init__(
            structuring_element=structuring_element,
            iterations=iterations)

    def apply(self, image):
        self.gray_scale_or_binary_check(image)
        return Image(cv2.erode(image, self._structuring_element, iterations=self._iterations), color_mode=image.color_mode)


class Dilation(_MorphologicalFilter):
    _default_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, structuring_element=_default_mask, iterations=1):
        super(Dilation, self).__init__(
            structuring_element=structuring_element,
            iterations=iterations)

    def apply(self, image):
        self.gray_scale_or_binary_check(image)
        return Image(cv2.dilate(image, self._structuring_element, iterations=self._iterations), color_mode=image.color_mode)


class Opening(_MorphologicalFilter):
    _default_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, structuring_element=None, iterations=1):
        super(Opening, self).__init__(
            structuring_element=structuring_element or self._default_mask,
            iterations=iterations)

    def apply(self, image):
        self.gray_scale_or_binary_check(image)
        return Image(
            cv2.morphologyEx(image, cv2.MORPH_OPEN, self._structuring_element, iterations=self._iterations),
            color_mode=image.color_mode
        )


class Closing(_MorphologicalFilter):
    _default_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, structuring_element=_default_mask, iterations=1):
        super(Closing, self).__init__(
            structuring_element=structuring_element,
            iterations=iterations)

    def apply(self, image):
        self.gray_scale_or_binary_check(image)
        return Image(
            cv2.morphologyEx(image, cv2.MORPH_CLOSE, self._structuring_element, iterations=self._iterations),
            color_mode=image.color_mode
        )


class GeodesicDilation(_MorphologicalFilter):
    _default_structuring_element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, mask_image, structuring_element=_default_structuring_element, iterations=1):
        super(GeodesicDilation, self).__init__(
            structuring_element=structuring_element,
            iterations=iterations)
        self.binary_check(mask_image)
        self._mask_image = mask_image
        self._dilation = Dilation(structuring_element=self._structuring_element)

    def apply(self, image):
        self.binary_check(image)
        for _ in range(self._iterations):
            image = self._apply_once(image)
        return image

    def _apply_once(self, marker_image):
        dilation = self._dilation.apply(marker_image)
        return Image(
            np.asarray(np.logical_and(dilation, self._mask_image), dtype=np.uint8),
            color_mode=ColorMode.binary
        )


class GeodesicErosion(_MorphologicalFilter):
    _default_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, mask_image, structuring_element=_default_mask, iterations=1):
        super(GeodesicErosion, self).__init__(
            structuring_element=structuring_element,
            iterations=iterations)
        self.binary_check(mask_image)
        self._mask_image = mask_image
        self._erosion= Erosion(structuring_element=self._structuring_element)

    def apply(self, image):
        self.binary_check(image)
        for _ in range(self._iterations):
            image = self._apply_once(image)
        return image

    def _apply_once(self, marker_image):
        erosion = self._erosion.apply(marker_image)
        return Image(
            np.asarray(np.logical_or(erosion, self._mask_image), dtype=np.uint8),
            color_mode=ColorMode.binary
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