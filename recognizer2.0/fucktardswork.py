import glob
import os

import progressbar

import inputOutput
import postprocessing, recognizer
from utils.image import Image


def get_words_files(data_directory):
    path = os.path.join(data_directory, '*.words')
    files = glob.glob(path)
    return files


def get_ppm_path(directory, words_file):
    base_name = remove_extension(words_file)
    ppm_file = add_extension(file_name=base_name, extension='ppm')
    return os.path.join(directory, ppm_file)


def remove_extension(file_path):
    _, file_name = os.path.split(words_file)
    base_name, _ = os.path.splitext(file_name)
    return base_name


def add_extension(file_name, extension):
    return '.'.join([file_name, extension])


def build_output_file(output_directory, words_file):
    base_name = remove_extension(words_file)
    output_file = add_extension(file_name=base_name, extension='words')
    return os.path.join(output_directory, output_file)


if __name__ == '__main__':
    data_directory = '/Users/laura/Downloads/subsettest2'
    output_directory = '/Users/laura/Desktop/output'

    words_files = get_words_files(data_directory)

    r = recognizer.Recognizer(
        postprocessor=postprocessing.NearestLexiconEntryWithPrior(
            distance_measure=postprocessing.distances.edit_distance
        )
    )

    bar = progressbar.ProgressBar()

    for words_file in bar(words_files):

        ppm_file = get_ppm_path(data_directory, words_file)

        annotation, _ = inputOutput.read(words_file)
        image = Image.from_file(ppm_file)

        try:
            r.recognize(image=image, annotation=annotation)
        except Exception:
            print "Could not handle {}".format(words_file)
            continue

        inputOutput.save(r.output_lines, build_output_file(output_directory, words_file))
