import argparse
import os.path

import annotationTree
import pageImage
import dataset

_image_file_extension = 'jpg'


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("imageDirectory", type=str,
                        help="the path to the directory with images")
    parser.add_argument("wordsFiles", nargs='+', type=str,
                        help="the words files, should be at least one file. Each words file should be associated with "
                             "an image in the imageDirectory.")
    return parser.parse_args()


def build_file_name(file_name, extension):
    return '.'.join([file_name, extension])


def build_file_path(path, file_name, extension=''):
    return os.path.join(path, build_file_name(file_name, extension))


if __name__ == "__main__":
    cli_arguments = parse_command_line_arguments()
    data_set = dataset.DataSet()

    for words_file in cli_arguments.wordsFiles:
        tree = annotationTree.AnnotationTree(file_path=words_file)
        image_file_name = tree.get_image_file_name()
        image_file_path = build_file_path(
            path=cli_arguments.imageDirectory,
            file_name=image_file_name,
            extension=_image_file_extension
        )
        page_image = pageImage.PageImage(image_file_path, tree)
        data_set.add(page_image, image_file_name)