import cv2
import numpy as np

import interface
import utils.image


class _MorphologicalFilter(interface.AbstractFilter):

    def __init__(self, structuring_element, iterations):
        super(_MorphologicalFilter, self).__init__()
        self._structuring_element = structuring_element
        self._iterations = iterations

    @classmethod
    def gray_scale_or_binary_check(cls, image):
        if image.color_mode not in [utils.image.ColorMode.gray, utils.image.ColorMode.binary]:
            raise utils.image.WrongColorModeError("This operation can only be performed on binary or gray scale images.")

    @classmethod
    def binary_check(cls, image):
        if image.color_mode is not utils.image.ColorMode.binary:
            raise utils.image.WrongColorModeError("This operation can only be performed on binary images.")


class Erosion(_MorphologicalFilter):
    _default_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, structuring_element=_default_mask, iterations=1):
        super(Erosion, self).__init__(
            structuring_element=structuring_element,
            iterations=iterations)

    def apply(self, image):
        self.gray_scale_or_binary_check(image)
        return utils.image.Image(cv2.erode(image, self._structuring_element, iterations=self._iterations), color_mode=image.color_mode)


class Dilation(_MorphologicalFilter):
    _default_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, structuring_element=_default_mask, iterations=1):
        super(Dilation, self).__init__(
            structuring_element=structuring_element,
            iterations=iterations)

    def apply(self, image):
        self.gray_scale_or_binary_check(image)
        return utils.image.Image(cv2.dilate(image, self._structuring_element, iterations=self._iterations), color_mode=image.color_mode)


class Opening(_MorphologicalFilter):
    _default_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, structuring_element=None, iterations=1):
        super(Opening, self).__init__(
            structuring_element=structuring_element or self._default_mask,
            iterations=iterations)

    def apply(self, image):
        self.gray_scale_or_binary_check(image)
        return utils.image.Image(
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
        return utils.image.Image(
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
        return utils.image.Image(
            np.asarray(np.logical_and(dilation, self._mask_image), dtype=np.float64),
            color_mode=utils.image.ColorMode.binary
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
        return utils.image.Image(
            np.asarray(np.logical_or(erosion, self._mask_image), dtype=np.float64),
            color_mode=utils.image.ColorMode.binary
        )


class _AbstractSimpleReconstructionFilter(_MorphologicalFilter):
    def __init__(self, structuring_element, operation):
        super(_AbstractSimpleReconstructionFilter, self).__init__(structuring_element=structuring_element, iterations=1)
        self._operation = operation

    def apply(self, image):
        new_image = self._operation.apply(image)
        while not (new_image == image).all():
            image, new_image = new_image, self._operation.apply(new_image)
        return image


class ReconstructionByErosion(_AbstractSimpleReconstructionFilter):
    _default_structuring_element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, mask_image, structuring_element=_default_structuring_element):
        super(ReconstructionByErosion, self).__init__(
            structuring_element=structuring_element,
            operation=GeodesicErosion(mask_image=mask_image, structuring_element=structuring_element))


class ReconstructionByDilation(_AbstractSimpleReconstructionFilter):
    _default_structuring_element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, mask_image, structuring_element=_default_structuring_element):
        super(ReconstructionByDilation, self).__init__(
            structuring_element=structuring_element,
            operation=GeodesicDilation(mask_image=mask_image, structuring_element=structuring_element))


class ReconstructionByOpening(_MorphologicalFilter):
    _default_structuring_element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, iterations=1, structuring_element=_default_structuring_element):
        super(ReconstructionByOpening, self).__init__(structuring_element=structuring_element, iterations=iterations)
        self.erosion = Erosion(iterations=self._iterations, structuring_element=self._structuring_element)

    def apply(self, image):
        erosion = self.erosion.apply(image)
        return ReconstructionByDilation(
            mask_image=image, structuring_element=self._structuring_element
        ).apply(erosion)


class ReconstructionByClosing(_MorphologicalFilter):
    _default_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def __init__(self, structuring_element=_default_mask, iterations=1):
        super(ReconstructionByClosing, self).__init__(
            structuring_element=structuring_element,
            iterations=iterations
        )
        self.dilation = Dilation(iterations=self._iterations, structuring_element=self._structuring_element)

    def apply(self, image):
        dilation = self.dilation.apply(image)
        return ReconstructionByErosion(
            mask_image=image, structuring_element=self._structuring_element
        ).apply(dilation)
