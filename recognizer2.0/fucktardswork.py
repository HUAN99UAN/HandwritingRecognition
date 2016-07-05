from copy import deepcopy
import argparse

import inputOutput
import postprocessing, recognizer
from utils.image import Image


def get_words_files(data_directory):
    raise NotImplementedError()
    return list()


def get_ppm_file(words_file):
    raise NotImplementedError()
    return str()


def build_output_file(output_directory):
    raise NotImplementedError()
    return str()

if __name__ == '__main__':
    data_directory = '/Users/laura/Downloads'
    output_directory = '/Users/laura/Desktop/output'

    words_files = get_words_files(data_directory)

    r = recognizer.Recognizer(
        postprocessor=postprocessing.NearestLexiconEntryWithPrior(
            distance_measure=postprocessing.distances.edit_distance
        )
    )

    for words_file in words_files:
        ppm_file = get_ppm_file(words_file)

        annotation, _ = inputOutput.read(words_file)
        image = Image.from_file(ppm_file)

        r.recognize(image=image, annotation=annotation)

        inputOutput.save(r.output_lines, build_output_file(output_directory))
