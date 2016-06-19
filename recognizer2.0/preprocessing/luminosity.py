import interface
import colorspaces
from utils.things import Range
from utils.image import Image, ColorMode


class LuminosityNormalization(interface.AbstractFilter):
    """Luminosity Normalization."""

    def __init__(self, square_size):
        super(LuminosityNormalization, self).__init__()
        self._square_size = square_size

    @property
    def _row_offset(self):
        return self._square_size.height / 2.0

    @property
    def _col_offset(self):
        return self._square_size.width / 2.0

    def apply(self, image):
        image = self.verify_image(image)
        new_luminosity_range = self._find_luminosity_range(image)
        current_luminosity_range = image.luminosity_range
        normalized_array = self._linear_scaling(image=image, old_range=current_luminosity_range, new_range=new_luminosity_range)
        return Image(normalized_array, color_mode=ColorMode.gray)

    @classmethod
    def verify_image(cls, image):
        if not image.color_mode.is_gray:
            image = colorspaces.ToGrayScale().apply(image)
        return image

    def _find_luminosity_range(self, image):
        center_rectangle = self._find_center_rectangle(image)
        minimum = center_rectangle.min()
        maximum = center_rectangle.max()
        return Range(min=minimum, max=maximum)

    def _find_center_rectangle(self, image):
        center_center = self._find_center(image)
        row_range = range(center_center.height - self._row_offset, center_center.height + self._row_offset + 1)
        col_range = range(center_center.width- self._col_offset, center_center.width + self._col_offset + 1)
        return self._extract_center_rectangle(image, row_range, col_range)

    @classmethod
    def _extract_center_rectangle(self, image, row_range, col_range):
        try:
            center_rectangle = image[row_range, col_range]
        except IndexError:
            row_range = self._fix_range(row_range, image.height)
            col_range = self._fix_range(col_range, image.width)
            center_rectangle = image[row_range, col_range]
        return center_rectangle

    @classmethod
    def _fix_range(self, range, maximum):
        if min(range) < 0:
            range_start = 0
        if max(range) > maximum:
            #Handle the [) effect of the python luminosity_range method.
            range_end = maximum + 1
        return range(range_start, range_end)

    @classmethod
    def _find_center(cls, image):
        return image.size / 2.0

    @classmethod
    def _linear_scaling(cls, image, old_range, new_range):
        old_range_length = old_range.max - old_range.min
        new_range_length = new_range.max - new_range.min
        normalized_to_old_min_image = image - old_range.min
        factor = (new_range_length / old_range_length)
        return normalized_to_old_min_image * factor + new_range.min

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
