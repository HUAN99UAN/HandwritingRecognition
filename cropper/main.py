import argparse
import os.path

import annotationTree
import pageImage

_image_file_extension = 'jpg'


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("wordsFile", help="the path to the words file")
    parser.add_argument("imageDirectory", help="the path to the directory with images")
    args = parser.parse_args()
    return args.wordsFile, args.imageDirectory


def build_file_name(file_name, extension):
    return '.'.join([file_name, extension])


def build_file_path(path, file_name, extension=''):
    return os.path.join(path, build_file_name(file_name, extension))


if __name__ == "__main__":
    (words_file, image_directory) = parse_command_line_arguments()
    words_file = wordsFile.WordsFile(words_file)