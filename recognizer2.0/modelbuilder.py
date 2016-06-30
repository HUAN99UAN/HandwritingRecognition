import argparse

import utils.actions as actions
import classification
import preprocessing
import featureExtraction


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('imageDirectory', type=str,
                        action=actions.ExpandDirectoryPathAction,
                        help='The path to the directory with images')
    parser.add_argument('wordsFiles', nargs='+', type=str, action=actions.ExpandFilePathsAction,
                        help='The words files, should be at least one file. Each words file should be associated with '
                             'an image in the imageDirectory.')
    parser.add_argument('--outputFile', type=str,
                        default=classification.default_model_file_path,
                        action=actions.ExpandFilePathAction,
                        help='The path to the output file.')
    return vars(parser.parse_args())

if __name__ == '__main__':
    cli_arguments = parse_command_line_arguments()
    write_model = classification.knn.KNN.build_model(
        xml_files=cli_arguments.get('wordsFiles'),
        image_directory=cli_arguments.get('imageDirectory'),
        preprocessor=preprocessing.Pipe(),
        feature_extractor=featureExtraction.Crossings(),
    )
    write_model.to_file(cli_arguments.get('outputFile'))