import argparse

import msgpack
import msgpack_numpy as m
import numpy as np

import interface
import utils.actions as actions
import config
from preprocessing.pipe import Pipe
from featureExtraction.crossings import Crossings
import utils.lists

m.patch()


class KNN(interface.AbstractClassifier):
    """Nearest Neighbour Classifier"""

    def __init__(self, model_file, k):
        super(KNN, self).__init__()
        self.k = k
        self._model = _Model.read_from_file(model_file)

    def classify(self, feature_vector):
        raise NotImplementedError()

    def build_model(self, xml_files, image_folder, preprocessor, feature_extractor):
        return _Model.build(
            xml_files=xml_files, image_folder=image_folder,
            preprocessor=preprocessor, feature_extractor=feature_extractor
        )

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class _Model(object):

    def __init__(self, keys=list(), values=list(), model=None):
        if model:
            self._model = model
        else:
            self._model = dict(zip(keys, values))

    def __getattr__(self, key):
        if key == '_model':
            # http://stackoverflow.com/a/5165352
            raise AttributeError()
        return getattr(self._model, key)

    @property
    def patterns_and_labels(self):
        labels = self._extract_label_vector()
        patterns = self._extract_pattern_matrix()
        return patterns, labels

    @property
    def number_of_feature_vectors(self):
        return sum([len(feature_vectors) for feature_vectors in self._model.values()])

    @property
    def dimensionality(self):
        random_feature_vector = self.get(self.keys()[0])[0]
        dim = random_feature_vector.shape[0]
        return dim

    def _extract_label_vector(self):
        labels = np.array(self._model.keys())
        number_of_feature_vectors_per_label = [len(feature_vectors) for feature_vectors in self._model.values()]
        return np.repeat(labels, number_of_feature_vectors_per_label, axis=0)

    def _extract_pattern_matrix(self):
        return np.array(
            utils.lists.flatten_one_level(
                [feature_vectors for feature_vectors in self.values()]
            )
        )

    @property
    def dictionary(self):
        return self._model

    @property
    def number_of_classes(self):
        return len(self._model.keys())

    @staticmethod
    def read_from_file(model_file):
        return _ModelReader(model_file).read()

    @staticmethod
    def build(self, xml_files, image_folder, preprocessor, feature_extractor):
        return _ModelBuilder(xml_files, image_folder, preprocessor, feature_extractor).build()

    def to_file(self, output_file):
        _ModelWriter(self, output_file=output_file).write()


class _ModelReader(object):

    def __init__(self, input_file):
        self._input_file = open(input_file, 'rb')

    def read(self):
        binary = self._input_file.read()
        model_dict = msgpack.unpackb(binary)
        self._input_file.close()
        return _Model(model=model_dict)


class _ModelWriter(object):

    def __init__(self, model, output_file):
        self._model = model
        self._output_file_name = output_file
        self._output_file = self.open_output_file()

    def open_output_file(self):
        return open(self._output_file_name, 'w+b')

    def write(self):
        binary = msgpack.packb(self._model.dictionary)
        self._output_file.write(binary)
        # pickle.dump(self._model, self._output_file)
        self._output_file.close()


class _ModelBuilder(object):

    def __init__(self, xml_files, image_folder, preprocessor, feature_extractor):
        self._xml_files = xml_files
        self._image_folder = image_folder
        self._preprocessor = preprocessor
        self._feature_extractor = feature_extractor

    def build(self):
        raise NotImplementedError()


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('imageDirectory', type=str,
                        action=actions.ExpandDirectoryPathAction,
                        help='The path to the directory with images')
    parser.add_argument('wordsFiles', nargs='+', type=str, action=actions.ExpandFilePathsAction,
                        help='The words files, should be at least one file. Each words file should be associated with '
                             'an image in the imageDirectory.')
    parser.add_argument('--outputFile', type=str,
                        default=config.model_file,
                        action=actions.ExpandFilePathAction,
                        help='The path to the output file.')
    return vars(parser.parse_args())

if __name__ == '__main__':
    cli_arguments = parse_command_line_arguments()
    model = KNN.build_model(
        xml_files=cli_arguments.get('wordsFiles'),
        image_folder=cli_arguments.get('imageDirectory'),
        preprocessor=Pipe(),
        feature_extractor=Crossings(),
    )
    model.to_file(cli_arguments.get('outputFile'))