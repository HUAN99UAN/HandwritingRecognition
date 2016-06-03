from collections import namedtuple
from errors.inputErrors import InvalidElementPageElementError

_BoundingBoxTuple = namedtuple('BoundingBox', ['left', 'top', 'right', 'bottom'])


class BoundingBox(_BoundingBoxTuple):
    def __new__(cls, left, top, right, bottom):
        self = super(BoundingBox, cls).__new__(cls, left, top, right, bottom)
        try:
            self._validate()
        except:
            raise
        return self

    @staticmethod
    def _dimension_greater_than_zero(dimension):
        return dimension > 0

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top

    def _is_valid(self):
        try:
            return BoundingBox._dimension_greater_than_zero(self.width) and \
                   BoundingBox._dimension_greater_than_zero(self.height)
        except:
            raise

    def _validate(self):
        if not self._is_valid():
            raise InvalidElementPageElementError(
                "the {} has invalid dimensions.".format(self))