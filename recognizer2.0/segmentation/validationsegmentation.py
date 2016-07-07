import segmentation.interface
from inputOutput import wordio as inputOutput
from recognizer import Recognizer
import postprocessing, segmentation
from utils.image import Image
from utils.things import BoundingBox
import inputOutput.wordio as wordio


def _read_file(words_file):
    if words_file:
        lines, _ = wordio.read(words_file)
        return lines


class ValidationSegmentation(segmentation.interface.AbstractSegmenter):
    """
    Segmenter that uses the provided bounding boxes to segment the image, to validate the classifier and
    feature extractor.

    Note that this segmenter ONLY works if the recognizer is called with ONE image!!
    """

    def __init__(self, annotation=None, annotation_file=None):
        super(ValidationSegmentation, self).__init__()
        annotation = annotation if annotation else _read_file(annotation_file)
        self._words = self._prepare_words(annotation)
        self._idx = 0

    def _prepare_words(self, annotation):
        bounding_boxes = list()
        for line in annotation:
            for word in line:
                bounding_boxes.append(self._shift_character_bounding_boxes(word))
        return bounding_boxes

    def _shift_character_bounding_boxes(self, word):
        character_bounding_boxes = list()
        for character in word.characters:
            shifted_bb = self._shifted_character_bounding_box(word, character)
            character_bounding_boxes.append(shifted_bb)
        return character_bounding_boxes

    @classmethod
    def _shifted_character_bounding_box(cls, word, character):
        horizontal_shift = word.left
        vertical_shift = word.top
        return BoundingBox(
            left=character.left - horizontal_shift,
            right=character.right - horizontal_shift,
            top=character.top - vertical_shift,
            bottom=character.bottom - vertical_shift
        )

    def segment(self, image):
        word = self._words[self._idx]
        self._idx += 1
        return self._segment_word_image(image, word)

    @classmethod
    def _segment_word_image(cls, image, word):
        character_images = list()
        for idx, character_bounding_box in enumerate(word):
            character_image = image.sub_image(character_bounding_box, remove_white_borders=True)
            character_images.append(character_image)
        return character_images


if __name__ == '__main__':
    annotation_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/input.words'
    image_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/input.ppm'
    annotation, _ = inputOutput.read(annotation_file)
    r = Recognizer(
        postprocessor=postprocessing.NearestLexiconEntryWithPrior(
            distance_measure=postprocessing.distances.edit_distance
        ),
        segmenter=segmentation.ValidationSegmentation(annotation=annotation)
    )

    image = Image.from_file(image_file)
    r.recognize(image=image, annotation=annotation)
    output_lines = r.output_lines
