import segmentation.binaryoversegmentation as config
import segmentation.binaryoversegmentation.baseline as baseline
import segmentation.binaryoversegmentation.segmentationlinesfilters as filters
import segmentation.binaryoversegmentation.strokewidth as strokewidth
import segmentation.interface
from segmentation.binaryoversegmentation.segmentationimage import SegmentationImage
from segmentation.binaryoversegmentation.suspiciousregions import SuspiciousRegionsComputer
import characterValidators
import continuesegmentationchecks
from utils.image import Image
from utils.shapes import Rectangle
from utils.things import Point, Size


class BinaryOverSegmentation(segmentation.interface.AbstractSegmenter):
    """Internal segmentation based on binary over segmentation.

    This method is based on Lee, Hong, and Brijesh Verma. "Binary segmentation algorithm for English cursive handwriting
    recognition." Pattern Recognition 45.4 (2012): 1306-1317.
    """

    def __init__(self,
                 base_line_estimator=baseline.VerticalHistogram(),
                 stroke_width_estimator=strokewidth.RasterTechnique(),
                 longest_word_length=13,
                 minimum_character_size=config.default_minimum_character_size,
                 maximum_character_size=config.default_maximum_character_size):

        super(BinaryOverSegmentation, self).__init__()
        self._max_segmentation = longest_word_length
        self._base_line_estimator = base_line_estimator
        self._stroke_width_estimator = stroke_width_estimator
        self._minimum_character_size = minimum_character_size
        self._maximum_character_size = maximum_character_size

        # Depend on the input image, but are handy to store in the object.
        self._low_base_line = None
        self._high_base_line = None
        self._stroke_width = None
        self._character_validators = self._build_character_validators()
        self._continue_segmentation_checks = self._build_continue_segmentation_checks()

    def segment(self, image):
        self._compute_parameters(image)
        segmentation_lines = self._compute_segmentation_lines(image)
        segmentation_image = SegmentationImage(
            image=image, segmentation_lines=segmentation_lines,
            character_validators=self._character_validators,
            continue_segmentation_checks=self._continue_segmentation_checks
        )
        return self._binary_segmentation(segmentation_image)

    def _compute_parameters(self, image):
        self._low_base_line, self._high_base_line = self._base_line_estimator.estimate(image)
        self._stroke_width = self._stroke_width_estimator.estimate(image)

    def _compute_segmentation_lines(self, image):
        suspicious_regions = self._compute_suspicious_regions(image)
        segmentation_lines = suspicious_regions.to_segmentation_lines(stroke_width=self._stroke_width)
        return self._filter_segmentation_lines(image=image, segmentation_lines=segmentation_lines)

    def _compute_suspicious_regions(self, image):
        body_region = image.sub_image(bounding_box=self._extract_body_bounding_box(image))
        suspicious_regions = SuspiciousRegionsComputer(threshold=self._stroke_width * 2).compute(body_region)
        return suspicious_regions

    def _extract_body_bounding_box(self, image):
        return Rectangle(
            top_left=Point(x=0, y=self._high_base_line.y),
            bottom_right=Point(x=image.width - 1, y=self._low_base_line.y)
        )

    @property
    def _minimum_num_foreground_pixels(self):
        return (self._high_base_line.y - self._low_base_line.y) * self._stroke_width

    def _build_character_validators(self):
        return [
            characterValidators.ValidateOnWidth(),
            characterValidators.ValidateOnForegroundPixels(),
        ]

    def _build_continue_segmentation_checks(self):
        return [
            continuesegmentationchecks.ContinueOnSSPCheck(),
            continuesegmentationchecks.ContinueOnWidthCheck(),
            continuesegmentationchecks.ContinueOnNumberOfForegroundPixels()
        ]

    def _continue_segmentation(self, done, to_do, idx):
        return all([
            len(done) < self._max_segmentation,
            bool(to_do),
            idx < self._max_segmentation
        ])


    @classmethod
    def _filter_segmentation_lines(cls, image, segmentation_lines):
        hole_filter = filters.HoleFilter(image=image)
        segmentation_lines = segmentation_lines.filter(hole_filter.keep)
        return segmentation_lines

    def _binary_segmentation(self, segmentation_image):
        def add_to_correct_list(image, position, done, segment_more):
            if image.is_empty:
                return
            elif image.is_valid_character_image:
                done.append((image, position))
                # image.show(wait_key=1000, window_name='Character')
            elif image.segment_further:
                segment_more.append((image, position))
                # image.show(wait_key=1000, window_name='Segment More')
            else:
                if image.width > config.character_width_distribution.mean and image.has_segmentation_lines:
                    segment_more.append((image, position))
                elif image.width < (config.character_width_distribution.mean - 2 * config.character_width_distribution.sd):
                    return
                else:
                    done.append((image, position))

        def select_next_image(images):
            images.sort(key=lambda (image, _): image.width_over_height_ratio)
            return images.pop()

        initial_position = 4611686018427387904  # 2^63
        character_images = list()
        images_for_further_segmentation = [(segmentation_image, initial_position)]

        idx = 0

        while self._continue_segmentation(character_images, images_for_further_segmentation, idx):
            segmentation_image, position = select_next_image(images_for_further_segmentation)

            (left, right) = segmentation_image.segment()

            add_to_correct_list(left, position=(position / 2.0),
                                done=character_images, segment_more=images_for_further_segmentation)
            add_to_correct_list(right, position=position,
                                done=character_images, segment_more=images_for_further_segmentation)
            idx += 1

        character_images.extend(images_for_further_segmentation)
        character_images.sort(key=lambda (_, position): position)
        return [image for (image, _) in character_images]

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


if __name__ == '__main__':
    from preprocessing.colorspaces import ToBinary

    image_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/word_2.png'
    image = Image.from_file(image_file)
    image = ToBinary().apply(image)

    characters = BinaryOverSegmentation().segment(image)

    # image.show(window_name='Word Image')

    # for (idx, character) in enumerate(characters):
    #     character.show(close_window=False, window_name="Character {}".format(idx))
