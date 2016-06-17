from copy import deepcopy
import argparse

import cv2
import numpy as np

import inputOutput
from inputOutput import actions
import classification, featureExtraction, postprocessing, segmentation, preprocessing
from utils.image import Image


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


def recognize(image, annotation, preprocessor, classifier, segmenter, postprocessor):
    raise NotImplementedError('Call the correct methods from the passed classes.')
    output_lines = []
    for line in lines:
        output_line = []
        for word in line:
            output_word = deepcopy(word)
            output_word.text = 'something'
            output_line.append(output_word)
        output_lines.append(output_line)

if __name__ == '__main__':
    cli_arguments = parse_command_line_arguments()
    annotation, _ = inputOutput.read(cli_arguments['words_file'])
    image = Image.from_file(cli_arguments['image'])

    raise NotImplementedError("Recognize isn't called, should be called here.")

    # output_lines = recognize(
    #     image=image,
    #     annotation=lines,
    #     preprocessor=,
    #     classifier=,
    #     segmenter=,
    #     postprocessor=,
    # )

    inputOutput.save(output_lines, cli_arguments['output_file'])