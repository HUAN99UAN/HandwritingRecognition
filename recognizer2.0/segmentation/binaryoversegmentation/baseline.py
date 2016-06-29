import numpy as np

from utils.statistics import mode
from utils.image import WrongColorModeError
from utils.shapes import HorizontalLine
from utils.mixins import CommonEqualityMixin


class _AbstractBaseLineEstimator(CommonEqualityMixin):

    def __init__(self):
        super(_AbstractBaseLineEstimator, self).__init__()

    def estimate(self, image):
        pass


class VerticalHistogram(_AbstractBaseLineEstimator):

    @classmethod
    def _verify_image(cls, image):
        if not image.color_mode.is_binary:
            raise WrongColorModeError("Expected a binary image.")

    def estimate(self, image):
        self._verify_image(image)
        (high_column_base_lines, low_column_base_lines) = (list(), list())
        transposed_image = image.T
        for column in transposed_image:
            indices = np.where(column == 0)
            if indices[0].size is not 0:
                high_column_base_lines.append(np.min(indices))
                low_column_base_lines.append(np.max(indices))

        low_base_line = HorizontalLine(x1=0, x2=image.width, y=mode(low_column_base_lines))
        high_base_line = HorizontalLine(x1=0, x2=image.width, y=mode(high_column_base_lines))
        return low_base_line, high_base_line
