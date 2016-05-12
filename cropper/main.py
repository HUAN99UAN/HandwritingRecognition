import argparse

import wordsFile


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("wordsFile", help="the path to the words file")
    parser.add_argument("imageDirectory", help="the path to the directory with images")
    args = parser.parse_args()
    return args.wordsFile, args.imageDirectory

if __name__ == "__main__":
    (words_file, image_directory) = parse_command_line_arguments()
    words_file = wordsFile.WordsFile(words_file)