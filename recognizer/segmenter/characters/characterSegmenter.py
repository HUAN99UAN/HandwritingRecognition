import warnings

from inputOutput.verifiers import WordImageVerifier
from segmenter.characters.SuspiciousSegmentationPointGenerator import SSPGenerator
from utils.functionArguments import merge_parameter_dictionaries
from utils.boundingBox import BoundingBox
from utils.decorators import lazy_property
from cropper.dataset import DataSet
import inputOutput.openers
from cropper.inputElements import CharacterImage


default_parameters = {
    'white_threshold': 240,
    'maximum_word_length': 10,
    'initial_segment_criterion': 50
}


class CharacterSegmenter:

    def __init__(self, word_image, parameters={}):
        """Class that segments characters based on the image of a word

        Args:
            image (PIL.Image): A gray scale image of a word
            [white_threshold (int): The white threshold to be used, gray scales lower than this value are foreground,
                gray values greater than this value are background.]
            [maximum_word_length (int): The length of the longest word in the training set.]
            [initial_segment_criterion (int): Parameter that determines the sensitivity of the segmentation process to
                the vertical histogram. High values results in more suspicious segmentation points.]
        """
        self._word_image = word_image
        self._parameters = merge_parameter_dictionaries(default=default_parameters, argument=parameters)
        try:
            validator = WordImageVerifier(self._word_image, **self._parameters).validate()
        except:
            raise
        self._bounding_boxes = self._get_bounding_boxes(self.segmentation_points)
        self._character_images = self._segment()

    @lazy_property
    def segmentation_points(self):
        return SSPGenerator(self._word_image, **self._parameters).suspicious_segmentation_points

    @property
    def base_lines(self):
        return SSPGenerator(self._word_image, **self._parameters).base_lines

    @property
    def character_images(self):
        return self._character_images

    @property
    def image(self):
        return self._word_image

    @property
    def bounding_boxes(self):
        return self._bounding_boxes

    def _segment(self):
        character_images = self._extract_characters(self.bounding_boxes)
        return character_images

    def _get_bounding_boxes(self, segmentation_points):
        def first_bounding_box(self, segmentation_points):
            bb = None
            try:
                bb = BoundingBox(left=0, right=segmentation_points[0].x,
                                   bottom=self._word_image.height, top=0)
            except:
                pass
            return bb

        def last_bounding_box(self, segmentation_points):
            bb = None
            try:
                bb = BoundingBox(left=segmentation_points.pop().x, right=self._word_image.width,
                               bottom=self._word_image.height, top=0)
            except:
                pass
            return bb

        bounding_boxes = list()
        if segmentation_points:
            first_bb = first_bounding_box(self, segmentation_points)
            if first_bb:
                bounding_boxes.append(first_bb)
            bounding_boxes.extend([
                BoundingBox(
                    left=left.x, right=right.x,
                    bottom=self._word_image.height, top=0)
                for (left, right)
                in zip(segmentation_points, segmentation_points[1:])
                if (left is not right)])
            last_bb = last_bounding_box(self, segmentation_points)
            if last_bb:
                bounding_boxes.append(last_bb)
        return bounding_boxes

    def _extract_characters(self, bounding_boxes):
        return [
            self._extract_character(bounding_box)
            for bounding_box
            in bounding_boxes
            ]

    def _extract_character(self, bounding_box):
        return self._word_image.crop(bounding_box)


class DataSetCharacterSegmenter:

    def __init__(self, data_set):
        self._data_set = data_set

    def segment(self):
        for _, page in self._data_set.pages():
            TreeCharacterSegmenter(tree=page).segment()


class TreeCharacterSegmenter:

    def __init__(self, tree):
        self._tree = tree

    def segment(self):
        for (_, word_image) in self._tree.words():
            WordImageSegmenter(word_image=word_image).segment()


class WordImageSegmenter:

    def __init__(self, word_image):
        self._word_image = word_image

    def segment(self):
        segmenter = CharacterSegmenter(word_image=self._word_image.preprocessed_image)
        images = segmenter.character_images
        bounding_boxes = segmenter.bounding_boxes
        character_images = self._create_character_images(images, bounding_boxes)
        self._word_image.children = self._create_children_dict(character_images)

    def _create_character_images(self, images, bounding_boxes):
        character_images = list()
        for ((image, bounding_box), number) in zip(zip(images, bounding_boxes), range(len(images))):
            character_images.append(
                CharacterImage(
                    parent=self._word_image,
                    image=image,
                    description=number,
                    bounding_box=bounding_box
                )
            )
        return character_images

    def _create_children_dict(self, children):
        return dict(
            zip(
                range(len(children)),
                children
            )
        )


if __name__ == '__main__':
    words_files = [
        '/Users/laura/Repositories/HandwritingRecognition/data/testdata/test_data/KNMP-VIII_F_69______2C2O_0004.words'
    ]
    image_directory = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/images'
    test_data = DataSet.from_files(words_files=words_files, image_files_directory=image_directory)

    DataSetCharacterSegmenter(data_set=test_data).segment()
    test_data.to_cropped_images_hierarchy('/Users/laura/Desktop/', extension='jpg')