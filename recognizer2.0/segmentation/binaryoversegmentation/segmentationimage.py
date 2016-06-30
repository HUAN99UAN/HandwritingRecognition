import operator

import numpy as np

from segmentation.binaryoversegmentation.imagesplitters import ForegroundPixelContourTracing
from utils.image import Image, ColorMode
from preprocessing.backgroundremoval import BackgroundBorderRemoval


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
        self._continue_segmentation_checks = getattr(obj, '_continue_segmentation_checks', list())
        self._image_splitter = getattr(obj, '_image_splitter', ForegroundPixelContourTracing())

    def segment(self):
        splitting_line = self.select_splitting_line()

        # image = self._segmentation_lines.paint_on(self, color=(0, 255, 0))
        # image = splitting_line.paint_on(image, color=(255, 0, 0))
        # image.show(wait_key=0, window_name='Segementation Image')
        return self._split_along(splitting_line)

    def select_splitting_line(self):
        # Number of black pixels underneath the segmentation_line
        pixel_density_scores = [self.pixel_column_density_at(line.x - 1) for line in self._segmentation_lines]

        # Distance to the vertical_center of the images
        distance_to_center_scores = self._compute_distance_to_center_scores()

        scores = [
            (1 - pixel_score) + distance_score
            for (pixel_score, distance_score)
            in zip(pixel_density_scores, distance_to_center_scores)
        ]
        max_index, _ = max(enumerate(scores), key=operator.itemgetter(1))
        return self._segmentation_lines.line_at_idx(max_index)

    def _compute_distance_to_center_scores(self):
        return [1 - (line.distance_to(self.vertical_center)/float(self.vertical_center))
                for line in self._segmentation_lines]

    def _split_along(self, line):
        return self._image_splitter.split(self, line)

    def pixel_column_density_at(self, x):
        return 1 - sum(self[:, x]) / (float(self.height) * 255)

    @property
    def is_valid_character_image(self):
        return all([validator.is_valid(self) for validator in self._character_validators])

    @property
    def has_segmentation_lines(self):
        return not self._segmentation_lines.is_empty

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
        return all([validator.continue_segmentation(self) for validator in self._continue_segmentation_checks])

    def show(self, wait_key=None, window_name=None, **kwargs):
        if not wait_key and not wait_key == 0:
            wait_key = super(SegmentationImage, self)._default_wait_key
        image_with_ssp = self._segmentation_lines.paint_on(self, **kwargs)
        if type(image_with_ssp) is SegmentationImage:
            # Brrrr
            image_with_ssp = Image(image_with_ssp, image_with_ssp.color_mode)
        image_with_ssp.show(wait_key=wait_key, window_name=window_name)

    def sub_image(self, bounding_box, remove_white_borders=True):
        """
        Returns the sub_image, the borders of the bounding box are null-indexed and inclusive!

        The validators are all copied. Only the segmentation lines that are still in the image are in
        the subimage. Indices of the bounding box work the same as the slicing indices, i.e. negative indices wrap
        around the iamge.

        :param bounding_box: Object with a top, bottom, left and right property.
        :return: A new segmentation image.
        """
        sub_image = super(SegmentationImage, self).sub_image(bounding_box, remove_white_borders=False)
        sub_image_segmentation_lines = self._segmentation_lines.get_subset_in(bounding_box)
        shift_distance = -1 * bounding_box.left
        sub_image_segmentation_lines = sub_image_segmentation_lines.shift_horizontally(shift_distance)
        new_image = SegmentationImage(
            image=sub_image,
            segmentation_lines=sub_image_segmentation_lines,
            character_validators=self._character_validators,
            continue_segmentation_checks=self._continue_segmentation_checks,
            image_splitter=self._image_splitter
        )
        if remove_white_borders:
            new_image = BackgroundBorderRemoval().apply(new_image)
        return new_image