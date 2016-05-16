import argparse

import dataset

default_output_extension = "jpg"


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("imageDirectory", type=str,
                        help="the path to the directory with images")
    parser.add_argument("wordsFiles", nargs='+', type=str,
                        help="the words files, should be at least one file. Each words file should be associated with "
                             "an image in the imageDirectory.")
    parser.add_argument("outputDirectory", type=str,
                        help="the path to the directory where you want to store the folders that represent pages. If "
                             "the folder does not exist it is created for you.")
    return parser.parse_args()

if __name__ == "__main__":
    cli_arguments = parse_command_line_arguments()
    data_set = dataset.DataSet.from_files(
        cli_arguments.wordsFiles,
        cli_arguments.imageDirectory)
    data_set.to_cropped_images_hierarchy(
        directory=cli_arguments.outputDirectory,
        extension=default_output_extension)
