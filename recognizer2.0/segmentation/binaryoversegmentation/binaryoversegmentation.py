import segmentation.binaryoversegmentation.baseline as baseline
import segmentation.binaryoversegmentation.segmentationlinesfilters as filters
import segmentation.binaryoversegmentation.strokewidth as strokewidth
import segmentation.interface
from postprocessing.lexicon import Lexicon
from segmentation.binaryoversegmentation.segmentationimage import SegmentationImage
from segmentation.binaryoversegmentation.suspiciousregions import SuspiciousRegionsComputer
from segmentation.binaryoversegmentation.characterValidators import ValidateOnWidth, ValidateOnForegroundPixels
from utils.image import Image
from utils.shapes import Rectangle
from utils.things import Point

red = (0, 0, 255)
blue = (255, 0, 0)


class BinaryOverSegmentation(segmentation.interface.AbstractSegmenter):
    """Internal segmentation based on binary over segmentation.

    This method is based on Lee, Hong, and Brijesh Verma. "Binary segmentation algorithm for English cursive handwriting
    recognition." Pattern Recognition 45.4 (2012): 1306-1317.
    """

    def __init__(self, lexicon,
                 base_line_estimator=baseline.VerticalHistogram(),
                 stroke_width_estimator=strokewidth.RasterTechnique()):

        super(BinaryOverSegmentation, self).__init__()
        self._lexicon = lexicon
        self._max_segmentation = lexicon.longest_word.length
        self._base_line_estimator = base_line_estimator
        self._stroke_width_estimator = stroke_width_estimator

        # Depend on the input image, but are handy to store in the object.
        self._low_base_line = None
        self._high_base_line = None
        self._stroke_width = None
        self._character_validators = list()
        self._continue_segmentation_checks = list()

    def segment(self, image):
        self._compute_parameters(image)
        segmentation_lines = self._compute_segmentation_lines(image)
        self._character_validators = self._build_character_validators()
        self._continue_segmentation_checks = self._build_continue_segmentation_checks()
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
            bottom_right=Point(x=image.width, y=self._low_base_line.y)
        )

    @property
    def minimum_num_foreground_pixels(self):
        return (self._high_base_line.y - self._low_base_line.y) * self._stroke_width

    def _build_character_validators(self):
        return [
            ValidateOnWidth(minimum_character_width=self._stroke_width),
            ValidateOnForegroundPixels(minimum_num_foreground_pixels=self.minimum_num_foreground_pixels)
        ]

    def _build_continue_segmentation_checks(self):
        raise NotImplementedError()
        return [

        ]

    @classmethod
    def _filter_segmentation_lines(cls, image, segmentation_lines):
        hole_filter = filters.HoleFilter(image=image)
        segmentation_lines = segmentation_lines.filter(hole_filter.keep)
        return segmentation_lines

    def _binary_segmentation(self, segmentation_image):
        def add_to_correct_list(image, done, segment_more):
            if image.segment_further:
                segment_more.append(image)
            elif image.is_valid_character_image:
                done.append(image)
            else:
                raise NotImplementedError(
                    "No way to handle images that are neither a valid character image or "
                    "should be segmented further."
                )

        def select_next_image(images):
            images.sort(key=lambda image: image.width_over_height_ratio)
            return images[0]

        character_images = list()
        images_for_further_segmentation = [segmentation_image]

        while len(character_images) < self._max_segmentation and images_for_further_segmentation:
            segmentation_image = select_next_image(images_for_further_segmentation)

            (left, right) = segmentation_image.segment()

            # segmentation_image.show(wait_key=0, window_name='')
            # left.show(wait_key=0, window_name='Left')
            # right.show(wait_key=0, window_name='Right')

            add_to_correct_list(left, character_images, images_for_further_segmentation)
            add_to_correct_list(right, character_images, images_for_further_segmentation)
        return character_images

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


if __name__ == '__main__':
    from preprocessing.colorspaces import ToBinary

    image_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/word_2.png'
    image = Image.from_file(image_file)
    image = ToBinary().apply(image)

    lexicon_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/lexicon.txt'
    lexicon = Lexicon.from_file(lexicon_file)

    BinaryOverSegmentation(lexicon=lexicon).segment(image)
