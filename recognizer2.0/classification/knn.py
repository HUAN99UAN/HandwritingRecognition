import argparse

import msgpack_numpy as m
from sklearn.neighbors import KNeighborsClassifier

import classification as config
import interface
import utils.actions as actions
from classification.model import GeneralModel
from featureExtraction.crossings import Crossings
from preprocessing.pipe import Pipe

m.patch()


class KNN(interface.AbstractClassifier):
    """Nearest Neighbour Classifier"""

    def __init__(self, model_file=config.default_model_file_path, k=1, model=None):
        super(KNN, self).__init__()
        if not model:
            model = GeneralModel.read_from_file(model_file)
        self._classifier = KNeighborsClassifier(n_neighbors=k, p=2, n_jobs=-1)
        (patterns, labels) = model.patterns_and_labels
        self._classifier.fit(patterns, labels)

    def classify(self, feature_vector):
        feature_vector = feature_vector.reshape(1, -1)
        return self._classifier.predict(feature_vector)

    @staticmethod
    def build_model(xml_files, image_directory, preprocessor, feature_extractor):
        return GeneralModel.build(
            xml_files=xml_files, image_directory=image_directory,
            preprocessor=preprocessor, feature_extractor=feature_extractor
        )

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('imageDirectory', type=str,
                        action=actions.ExpandDirectoryPathAction,
                        help='The path to the directory with images')
    parser.add_argument('wordsFiles', nargs='+', type=str, action=actions.ExpandFilePathsAction,
                        help='The words files, should be at least one file. Each words file should be associated with '
                             'an image in the imageDirectory.')
    parser.add_argument('--outputFile', type=str,
                        default=config.default_model_file_path,
                        action=actions.ExpandFilePathAction,
                        help='The path to the output file.')
    return vars(parser.parse_args())

if __name__ == '__main__':
    cli_arguments = parse_command_line_arguments()
    write_model = KNN.build_model(
        xml_files=cli_arguments.get('wordsFiles'),
        image_directory=cli_arguments.get('imageDirectory'),
        preprocessor=Pipe(),
        feature_extractor=Crossings(),
    )
    write_model.to_file(cli_arguments.get('outputFile'))