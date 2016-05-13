import argparse

import dataset

def parse_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("imageDirectory", type=str,
                        help="the path to the directory with images")
    parser.add_argument("wordsFiles", nargs='+', type=str,
                        help="the words files, should be at least one file. Each words file should be associated with "
                             "an image in the imageDirectory.")
    return parser.parse_args()

if __name__ == "__main__":
    cli_arguments = parse_command_line_arguments()
    data_set = dataset.DataSet.from_files(
        cli_arguments.wordsFiles,
        cli_arguments.imageDirectory)
    print(data_set)