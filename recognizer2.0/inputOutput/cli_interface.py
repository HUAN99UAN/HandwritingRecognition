import argparse

import utils.actions as actions
import classification

def parse_imagedir_wordsfiles_optionaloutputFile(default_output_file):
    parser = argparse.ArgumentParser()
    parser.add_argument('imageDirectory', type=str,
                        action=actions.ExpandDirectoryPathAction,
                        help='The path to the directory with images')
    parser.add_argument('wordsFiles', nargs='+', type=str, action=actions.ExpandFilePathsAction,
                        help='The words files, should be at least one file. Each words file should be associated with '
                             'an image in the imageDirectory.')
    parser.add_argument('--outputFile', type=str,
                        default=default_output_file,
                        action=actions.ExpandFilePathAction,
                        help='The path to the output file.')
    arguments = vars(parser.parse_args())
    return arguments['imageDirectory'], arguments['wordsFiles'], arguments['outputFile']