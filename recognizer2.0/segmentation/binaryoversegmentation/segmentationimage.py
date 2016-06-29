import numpy as np

from segmentation.binaryoversegmentation.imagesplitters import ForegroundPixelContourTracing
from utils.image import Image, ColorMode


class SegmentationImage(Image):
    """An image that is being segmented"""

    def __new__(cls, image, segmentation_lines, character_validators=[], continue_segmentation_checks=[], image_splitter=ForegroundPixelContourTracing()):
        obj = Image.__new__(cls, image, image.color_mode)
        obj._segmentation_lines = segmentation_lines
        obj._character_validators = character_validators
        obj._continue_segmentation_checks = continue_segmentation_checks
        obj._image_splitter = image_splitter
        return obj

    def __array_finalize__(self, obj):
        super(SegmentationImage, self).__array_finalize__(obj)
        self._segmentation_lines = getattr(obj, '_segmentation_lines', list())
        self._character_validators = getattr(obj, '_character_validators', list())
        self._continue_segmentation_checks = getattr(obj, '__continue_segmentation_checks', list())
        self._image_splitter = getattr(obj, '_image_splitter', ForegroundPixelContourTracing())

    def segment(self):
        splitting_line = self._segmentation_lines.line_closest_to(self.vertical_center)

        image = splitting_line.paint_on(self, color=(255, 0, 0))
        return self._split_along(splitting_line)

    def _split_along(self, line):
        return self._image_splitter.split(self, line)

    @property
    def is_valid_character_image(self):
        return all([validator.is_valid(self) for validator in self._character_validators])

    @property
    def has_segmentation_lines(self):
        return bool(self._segmentation_lines)

    @property
    def width_over_height_ratio(self):
        return float(self.width) / float(self.height)

    @property
    def number_of_foreground_pixels(self):
        if self.color_mode in [ColorMode.gray, ColorMode.bgr]:
            raise NotImplementedError("Number of foreground pixel is only supported for binary images.")
        else:
            return np.sum(np.array(self))

    @property
    def segment_further(self):
        return all([validator.is_valid(self) for validator in self._continue_segmentation_checks])

    def show(self, wait_key=None, window_name=None, **kwargs):
        if not wait_key and not wait_key == 0:
            wait_key = super(SegmentationImage, self)._default_wait_key
        image_with_ssp = self._segmentation_lines.paint_on(self, **kwargs)
        image_with_ssp.show(wait_key=wait_key, window_name=window_name)

    def sub_image(self, bounding_box):
        """
        Returns the sub_image, the borders of the bounding box are null-indexed and inclusive!

        The validators are all copied. Only the segmentation lines that are still in the image are in
        the subimage. Indices of the bounding box work the same as the slicing indices, i.e. negative indices wrap
        around the iamge.

        :param bounding_box: Object with a top, bottom, left and right property.
        :return: A new segmentation image.
        """
        def validate_bounding_box(image, bounding_box):
            if bounding_box.left < 0:
                raise IndexError()
            if bounding_box.right >= image.width:
                raise IndexError()
            if bounding_box.top < 0:
                raise IndexError()
            if bounding_box.bottom >= image.height:
                raise IndexError()

        validate_bounding_box(self, bounding_box)
        sub_image_pixels = self[
                           bounding_box.top:(bounding_box.bottom+1),
                           bounding_box.left:(bounding_box.right+1)
                           ]
        sub_image_segmentation_lines = self._segmentation_lines.get_subset_in(bounding_box)
        shift_distance = -1 * bounding_box.left
        sub_image_segmentation_lines = sub_image_segmentation_lines.shift_horizontally(shift_distance)
        return SegmentationImage(
            image=sub_image_pixels,
            segmentation_lines=sub_image_segmentation_lines,
            character_validators=self._character_validators,
            continue_segmentation_checks=self._continue_segmentation_checks,
            image_splitter=self._image_splitter
        )

    def dumps(self):
        super(SegmentationImage, self).dumps()
