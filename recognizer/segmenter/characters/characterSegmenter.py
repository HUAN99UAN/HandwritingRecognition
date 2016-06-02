from inputOutput.verifiers import WordImageVerifier
from segmenter.characters.SuspiciousSegmentationPointGenerator import SSPGenerator
from utils.functionArguments import merge_parameter_dictionaries
from utils.boundingBox import BoundingBox
from utils.decorators import lazy_property

default_parameters = {
    'white_threshold': 240,
    'longest_word_length': 10,
    'initial_segment_criterion': 50
}


class CharacterSegmenter:

    def __init__(self, word_image, parameters={}):
        """Class that segments characters based on the image of a word

        Args:
            image (PIL.Image): A gray scale image of a word
            [white_threshold (int): The white threshold to be used, gray scales lower than this value are foreground,
                gray values greater than this value are background.]
            [longest_word_length (int): The length of the longest word in the training set.]
            [initial_segment_criterion (int): Parameter that determines the sensitivity of the segmentation process to
                the vertical histogram. High values results in more suspicious segmentation points.]
        """
        self._word_image = word_image
        self._parameters = merge_parameter_dictionaries(default=default_parameters, argument=parameters)
        try:
            validator = WordImageVerifier(self._word_image, **self._parameters).validate()
        except:
            raise
        self._segment()

    @lazy_property
    def segmentation_points(self):
        return SSPGenerator(self._word_image, **self._parameters).suspicious_segmentation_points

    def _segment(self):
        bounding_boxes = self._get_bounding_boxes(self.segmentation_points)
        characters = self._extract_characters(bounding_boxes)
        return characters

    def _get_bounding_boxes(self, segmentation_points):
        def first_bounding_box(self, segmentation_points):
            return BoundingBox(left=0, right=segmentation_points[0].x,
                               bottom=self._word_image.height, top=0)

        def last_bounding_box(self, segmentation_points):
            return BoundingBox(left=segmentation_points.pop().x, right=self._word_image.width,
                               bottom=self._word_image.height, top=0)

        bounding_boxes = [first_bounding_box(self, segmentation_points)]
        bounding_boxes.extend([
            BoundingBox(
                left=left.x, right=right.x,
                bottom=self._word_image.height, top=0)
            for (left, right)
            in zip(segmentation_points, segmentation_points[1:])
            ])
        bounding_boxes.append(last_bounding_box(self, segmentation_points))
        return bounding_boxes

    def _extract_characters(self, bounding_boxes):
        return [
            self._extract_character(bounding_box)
            for bounding_box
            in bounding_boxes
            ]

    def _extract_character(self, bounding_box):
        return self._word_image.crop(bounding_box)