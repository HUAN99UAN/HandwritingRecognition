import argparse
from os import path

import msgpack
import msgpack_numpy as m
import numpy as np

import config
import inputOutput.wordio as xmlReader
import interface
import utils.actions as actions
import utils.lists
from featureExtraction.crossings import Crossings
from preprocessing.pipe import Pipe
from utils.image import Image

m.patch()


class KNN(interface.AbstractClassifier):
    """Nearest Neighbour Classifier"""

    def __init__(self, model_file, k):
        super(KNN, self).__init__()
        self.k = k
        self._model = _Model.read_from_file(model_file)

    def classify(self, feature_vector):
        raise NotImplementedError()

    @staticmethod
    def build_model(xml_files, image_directory, preprocessor, feature_extractor):
        return _Model.build(
            xml_files=xml_files, image_directory=image_directory,
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
    def build(xml_files, image_directory, preprocessor, feature_extractor):
        return _ModelBuilder(xml_files, image_directory, preprocessor, feature_extractor).build()

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

    def __init__(self, xml_files, image_directory, preprocessor, feature_extractor, image_extension='ppm'):
        self._xml_files = xml_files
        self._image_directory = image_directory
        self._preprocessor = preprocessor
        self._feature_extractor = feature_extractor
        self._image_extension = image_extension
        self._model = dict()

    def build(self):
        for xml_file in self._xml_files:
            self._add_features_from_file(xml_file)
        return _Model(model=self._model)

    def _add_features_from_file(self, xml_file):
        image, lines = self._get_image_and_lines_from_file(xml_file)
        preprocessed_image = self._preprocessor.apply(image)
        for line in lines:
            self._add_features_from_line(line=line, image=preprocessed_image)

    def _get_image_and_lines_from_file(self, xml_file):
        lines, image_name = xmlReader.read(xml_file)
        image_path = self._build_image_file_path(image_name)
        image = Image.from_file(image_path)
        return image, lines

    def _build_image_file_path(self, image_name):
        return path.join(self._image_directory, image_name + '.' + self._image_extension)

    def _add_features_from_line(self, line, image):
        for word in line:
            self._add_features_from_word(word, image)

    def _add_features_from_word(self, word, image):
        for character in word.characters:
            self._add_feature_from_character(character, image)

    def _add_feature_from_character(self, character, image):
        character_image = image.sub_image(character, remove_white_borders=True)
        self._add_feature_vector(
            label=character.text,
            feature_vector=self._feature_extractor.extract(character_image)
        )

    def _add_feature_vector(self, label, feature_vector):
        if self._model.has_key(label):
            self._model.get(label).append(feature_vector)
        else:
            self._model[label] = [feature_vector]


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('imageDirectory', type=str,
                        action=actions.ExpandDirectoryPathAction,
                        help='The path to the directory with images')
    parser.add_argument('wordsFiles', nargs='+', type=str, action=actions.ExpandFilePathsAction,
                        help='The words files, should be at least one file. Each words file should be associated with '
                             'an image in the imageDirectory.')
    parser.add_argument('--outputFile', type=str,
                        default=config.write_model_file,
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