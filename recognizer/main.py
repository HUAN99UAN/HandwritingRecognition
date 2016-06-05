import argparse
import os
import fnmatch

from cropper.dataset import DataSet
from preprocessor import pipe
from segmenter.characters.characterSegmenter import DataSetCharacterSegmenter
from extractor.characterFeatureExtraction import CharacterFeatureExtraction


def recursive_search(directory, ext='words'):
    matches = []
    for root, _, file_names in os.walk(directory):
        for filename in fnmatch.filter(file_names, '*.'+ext):
            matches.append(os.path.join(root, filename))
    return matches


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Read the input for the classification of handwritten text.')

    parser.add_argument('word_test_dir', metavar='wrdTest', type=str,
                        help='directory for the test images (words)')

    parser.add_argument('word_training_dir', metavar='wrdTrain', type=str,
                        help='directory for the trainning images (words)')

    parser.add_argument('xml_test_dir', metavar='xmlTest', type=str,
                        help='directory for the labeled xml (words)')

    parser.add_argument('xml_training_dir', metavar='xmlTrain', type=str,
                        help='directory for the labeled xml (characters)')
    return vars(parser.parse_args())


def remove_noise_from(data_set):
    for _, page in data_set.pages():
        page.preprocessed_np_array = pipe.pipe().pipe_line(page.image_as_np_array)


def extract_features(data_set):
    for _, character in data_set.characters():
        character.feature_vector = CharacterFeatureExtraction.extract(character.preprocessed_np_array)

if __name__ == '__main__':
    arguments = parse_command_line_arguments()

    xml_test_files = recursive_search(arguments['xml_test_dir'])

    test_data = DataSet.from_files(
        words_files=xml_test_files,
        image_files_directory=arguments['word_test_dir']
    )

    remove_noise_from(test_data)

    DataSetCharacterSegmenter(data_set=test_data).segment()

    extract_features(test_data)

    # call classifier somewhere somehow









