import numpy as np
from cv2 import equalizeHist

import interface
import colorspaces
from utils.things import Size
import utils.image


class LuminosityNormalization(interface.AbstractFilter):
    """Luminosity Normalization."""

    _default_rectangle_size = Size(width=500, height=500)

    def __init__(self, rectangle_size=_default_rectangle_size):
        super(LuminosityNormalization, self).__init__()
        self._rectangle_size = rectangle_size

    @property
    def _row_offset(self):
        return self._rectangle_size.height / 2

    @property
    def _col_offset(self):
        return self._rectangle_size.width / 2

    def apply(self, image):
        image = self.verify_image(image)
        center_rectangle = self._find_center_rectangle(image)
        return self._linear_scaling(
            image=image,
            old_range=image.luminosity_range,
            new_range=center_rectangle.luminosity_range
        )

    @classmethod
    def verify_image(cls, image):
        if not image.color_mode.is_gray:
            image = colorspaces.ToGrayScale().apply(image)
        return image

    def _find_center_rectangle(self, image):
        center = self._find_center(image)
        low_row_idx, high_row_idx = self._compute_range(image.height, center.height, self._row_offset)
        low_col_idx, high_col_idx = self._compute_range(image.width, center.width, self._col_offset)
        return image[
                low_row_idx:high_row_idx,
                low_col_idx:high_col_idx
            ]

    @classmethod
    def _compute_range(cls, image_size, center, offset):
        low_idx = max(0, center - offset)
        high_idx = min(center + offset + 1, image_size)
        return low_idx, high_idx

    @classmethod
    def _find_center(cls, image):
        return image.dimension / 2

    @classmethod
    def _linear_scaling(cls, image, old_range, new_range):
        normalized_to_old_min_image = image - old_range.min
        factor = (new_range.length / float(old_range.length))
        return utils.image.Image(
            np.asarray(normalized_to_old_min_image * factor + new_range.min, dtype=np.uint8),
            color_mode=utils.image.ColorMode.gray)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class HistogramsEqualization(interface.AbstractFilter):

    def __init__(self):
        super(HistogramsEqualization, self).__init__()

    @classmethod
    def verify_image(cls, image):
        if not image.color_mode.is_gray:
            image = colorspaces.ToGrayScale().apply(image)
        return image

    def apply(self, image):
        image = self.verify_image(image)
        image_array = self._linear_scaling(image=image)
        return utils.image.Image(image_array, color_mode=image.color_mode)

    @classmethod
    def _linear_scaling(cls, image):
        return equalizeHist(image)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)



