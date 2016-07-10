from os import path

import msgpack
import numpy as np

import utils.lists
from inputOutput import wordio as xmlReader
from utils.image import Image


class GeneralModel(object):

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
    def classes(self):
        for item in self._model:
            yield self._model.get(item)

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
        return GeneralModel(model=model_dict)


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
        return GeneralModel(model=self._model)

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
        if not character.is_valid:
            # character_image = image.sub_image(character, remove_white_borders=True)
            # character_image.show(wait_key=500)
            return
        character_image = image.sub_image(character, remove_white_borders=True)
        if not character_image.is_empty:
            self._add_feature_vector(
                label=character.text,
                feature_vector=self._feature_extractor.extract(character_image)
            )

    def _add_feature_vector(self, label, feature_vector):
        if self._model.has_key(label):
            self._model.get(label).append(feature_vector)
        else:
            self._model[label] = [feature_vector]