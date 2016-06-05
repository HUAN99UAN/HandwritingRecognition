import argparse
import pickle

import utils.actions
import cropper.dataset
from preprocessor import pipe
from extractor.characterFeatureExtraction import CharacterFeatureExtraction
import config

class Model(object):

    def __init__(self, keys=[], values=[], model=None):
        if model:
            self._model = model
        else:
            self._model = dict(zip(keys, values))

    def to_file(self, output_file):
        _ModelWriter(model=self, output_file=output_file).write()

    def __getattr__(self, key):
        if key == '_model':
            # http://stackoverflow.com/a/5165352
            raise AttributeError()
        return getattr(self._model, key)

    def merge_with(self, other):
        keys = set(self.keys()).union(other.keys())
        empty_list = []
        self._model = dict(
            (key, self.get(key, empty_list) + other.get(key, empty_list))
            for key
            in keys
        )

    @property
    def number_of_classes(self):
        return len(self._model.keys())

    @staticmethod
    def build_from_files(word_files, image_directory):
        return _ModelBuilder(word_files, image_directory).build()

    @staticmethod
    def from_file(model_file):
        return _ModelReader(input_file=model_file).read()


class _ModelBuilder(object):

    def __init__(self, word_files, image_directory):
        self._data_set = cropper.dataset.DataSet.from_files(
            words_files=word_files,
            image_files_directory=image_directory
        )
        self._pre_processor = pipe.pipe().pipe_line
        self._feature_extractor = CharacterFeatureExtraction().extract

    def build(self):
        self._data_set.pre_process(self._pre_processor)
        self._data_set.extract_features(self._feature_extractor)
        return self._data_set.to_model()


class _ModelWriter(object):

    def __init__(self, model, output_file):
        self._model = model
        self._output_file_name = output_file
        self._output_file = self.open_output_file()

    def open_output_file(self):
        return open(self._output_file_name, 'w+b')

    def write(self):
        pickle.dump(self._model, self._output_file)
        self._output_file.close()


class _ModelReader(object):

    def __init__(self, input_file):
        self._input_file = open(input_file, 'rb')

    def read(self):
        model = pickle.load(self._input_file)
        self._input_file.close()
        return model


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('imageDirectory', type=str,
                        action=utils.actions.ExpandDirectoryPathAction,
                        help='The path to the directory with images')
    parser.add_argument('wordsFiles', nargs='+', type=str, action=utils.actions.ExpandFilePathsAction,
                        help='The words files, should be at least one file. Each words file should be associated with '
                             'an image in the imageDirectory.')
    parser.add_argument('--outputFile', type=str,
                        default=config.model_file,
                        action=utils.actions.ExpandFilePathAction,
                        help='The path to the output file.')
    return vars(parser.parse_args())


if __name__ == '__main__':
    cli_arguments = parse_command_line_arguments()
    model = Model.build_from_files(
        word_files=cli_arguments.get('wordsFiles'),
        image_directory=cli_arguments.get('imageDirectory'))
    model.to_file(cli_arguments.get('outputFile'))
    # read_model = Model.from_file(cli_arguments.get('outputFile'))