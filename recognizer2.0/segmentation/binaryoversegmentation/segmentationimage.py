from utils import image
from utils.image import Image
from segmentation.binaryoversegmentation.imagesplitters import ForegroundPixelContourTracing


class SegmentationImage(Image):
    """An image that is being segmented"""

    def __new__(cls, image, segmentation_lines, validators=[], image_splitter=ForegroundPixelContourTracing()):
        obj = Image.__new__(cls, image, image.color_mode)
        obj._segmentation_lines = segmentation_lines
        obj._validators = validators
        obj._image_splitter = image_splitter
        return obj

    def __array_finalize__(self, obj):
        super(SegmentationImage, self).__array_finalize__(obj)
        self._segmentation_lines = getattr(obj, '_segmentation_lines', list())
        self._validators = getattr(obj, '_validators', list())
        self._image_splitter = getattr(obj, '_image_splitter', ForegroundPixelContourTracing())

    def segment(self):
        splitting_line = self._segmentation_lines.line_closest_to(self.vertical_center)
        return self._split_along(splitting_line)

    def _split_along(self, line):
        return self._image_splitter.split(self, line)

    @property
    def is_valid_character_image(self):
        all([validator.is_valid(self) for validator in self._validators])

    @property
    def has_segmentation_lines(self):
        return bool(self._segmentation_lines)

    @property
    def width_over_height_ratio(self):
        return self.width / self.height

    @property
    def segment_further(self):
        raise NotImplementedError()
        # width < MinimumCharacterWidth + AverageCharacterWidth
        # Still has some SSP's left

    def show(self, wait_key=None, window_name=None, **kwargs):
        if not wait_key and not wait_key == 0:
            wait_key = super(SegmentationImage, self)._default_wait_key
        image_with_ssp = self._segmentation_lines.paint_on(self, **kwargs)
        image_with_ssp.show(wait_key=wait_key, window_name=window_name)

    def sub_image(self, bounding_box):
        sub_image_pixels = self[bounding_box.top:bounding_box.bottom, bounding_box.left:bounding_box.right]
        sub_image_segmentation_lines = self._segmentation_lines.get_subset_in(bounding_box)
        return SegmentationImage(
            image=sub_image_pixels,
            segmentation_lines=sub_image_segmentation_lines,
            validators=self._validators,
            image_splitter=self._image_splitter
        )

    def dumps(self):
        super(SegmentationImage, self).dumps()

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class _AbstractSegmentationImageValidator(object):

    def __init__(self):
        super(_AbstractSegmentationImageValidator, self).__init__()

    def is_valid(self, image):
        pass

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class ValidateOnWidth(_AbstractSegmentationImageValidator):
    def __init__(self, minimum_character_width):
        _AbstractSegmentationImageValidator.__init__(self)
        self._minimum_character_width = minimum_character_width

    def is_valid(self, image):
        return image.width > self._minimum_character_width


class ValidateOnForegroundPixels(_AbstractSegmentationImageValidator):
    def __init__(self, minimum_num_foreground_pixels):
        _AbstractSegmentationImageValidator.__init__(self)
        self._minimum_num_foreground_pixels = minimum_num_foreground_pixels

    def is_valid(self, image):
        return image.number_of_foreground_pixels> self._minimum_num_foreground_pixels