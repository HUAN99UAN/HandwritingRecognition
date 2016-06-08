import argparse
import xml.etree.ElementTree as et

import utils.actions
from cropper.dataset import DataSet
from preprocessor import pipe
from segmenter.characters.characterSegmenter import DataSetCharacterSegmenter
from extractor.characterFeatureExtraction import CharacterFeatureExtraction
from classifier.classifier import Classifier

import model
import config


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Read the input for the classification of handwritten text.')

    parser.add_argument('words_file', metavar='wordsFile', type=str,
                        action=utils.actions.ExpandFilePathAction,
                        help='The words file')

    parser.add_argument('image', metavar='image', type=str,
                        action=utils.actions.ExpandFilePathAction,
                        help='The image with the text that is to be read.')

    parser.add_argument('outputFilePath', metavar='outputWordsFile', type=str,
                        action=utils.actions.ExpandFilePathAction,
                        help='The path output file.')
    return vars(parser.parse_args())


def remove_noise_from(data_set):
    for _, page in data_set.pages():
        page.preprocessed_np_array = pipe.pipe().pipe_line(page.image_as_np_array)

def extract_features(data_set):
    for _, character in data_set.characters():
        character.feature_vector = CharacterFeatureExtraction().extract(character.preprocessed_np_array)


def classify_feature_vectors(data_set, classifier):
    for _, character in data_set.characters():
        classification = classifier.knn(character)
        character.text = classification[0]


if __name__ == '__main__':
    arguments = parse_command_line_arguments()

    test_data = DataSet.test_data(
        words_file=arguments.get('words_file'),
        image_file=arguments.get('image')
    )

    remove_noise_from(test_data)

    DataSetCharacterSegmenter(data_set=test_data).segment()

    extract_features(data_set=test_data)

    model = model.Model.from_file(model_file=config.model_file)

    c = Classifier(model=model)

    classify_feature_vectors(data_set=test_data, classifier=c)

    test_data.write_annotation_trees_to_file(
        file_names=[arguments.get('outputFilePath')],
        updated=True
    )