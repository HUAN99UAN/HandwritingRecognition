from copy import deepcopy
import argparse

import cv2
import numpy as np

import inputOutput
from inputOutput import actions
import classification, featureExtraction, postprocessing, segmentation, preprocessing
from utils.image import Image


class Recognizer(object):

    def __init__(self,
                 preprocessor=preprocessing.Pipe(),
                 segmenter=segmentation.BinaryOverSegmentation(),
                 feature_extractor=featureExtraction.Crossings(),
                 classifier=classification.KNN(),
                 postprocessor=postprocessing.NearestLexiconEntry()):
        self._pre_processor = preprocessor
        self._segmenter = segmenter
        self._feature_extractor = feature_extractor
        self._classifier = classifier
        self._post_processor = postprocessor

        self._output_lines = list()

    @property
    def output_lines(self):
        return self._output_lines

    def recognize(self, image, annotation):
        pre_processed_image = self._pre_processor.apply(image)
        for line in annotation:
            output_line = self._recognize_line(line, pre_processed_image)
            self._output_lines.append(output_line)

    def _recognize_line(self, line, image):
        output_line = list()
        for word in line:
            word_image = image.sub_image(word)
            word_text = self._recognize_word(word_image)
            output_word = deepcopy(word)
            output_word.text = word_text
            output_line.append(output_word)
        return output_line

    def _recognize_word(self, word_image):
        character_images = self._segmenter.segment(word_image)
        characters = list()
        for character_image in character_images:
            characters.append(self._recognize_character(character_image))
        return self._post_processor.process(''.join(characters))

    def _recognize_character(self, character_image):
        feature_vector = self._feature_extractor.extract(character_image)
        classification = self._classifier.classify(feature_vector)
        return classification


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Read the input for the classification of handwritten text.')

    parser.add_argument('image', metavar='image', type=str,
                        action=actions.ExpandFilePathAction,
                        help='The image with the text that is to be read.')
    parser.add_argument('words_file', metavar='wordsFile', type=str,
                        action=actions.ExpandFilePathAction,
                        help='The words file')
    parser.add_argument('output_file', metavar='outputWordsFile', type=str,
                        action=actions.OutputFileAction,
                        help='The path output file.')
    return vars(parser.parse_args())

if __name__ == '__main__':
    cli_arguments = parse_command_line_arguments()
    annotation, _ = inputOutput.read(cli_arguments['words_file'])
    image = Image.from_file(cli_arguments['image'])

    r = Recognizer(
        postprocessor=postprocessing.NearestLexiconEntryWithPrior(
            distance_measure=postprocessing.distances.edit_distance
        )
    )
    r.recognize(image=image, annotation=annotation)

    inputOutput.save(r.output_lines, cli_arguments['output_file'])