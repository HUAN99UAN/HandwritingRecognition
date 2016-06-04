from cropper.dataset import DataSet
from preprocessor import pipe
from extractor.characterFeatureExtraction import characterFeatureExtraction


class Model(object):

    def __init__(self, keys=[], values=[], model=None):
        if not model:
            self._model = model
        else:
            self._model = dict(zip(keys, values))

    def serialize(self):
        pass

    def to_file(self, file):
        pass

    def __getattr__(self, key):
        if key == '_model':
            # http://stackoverflow.com/a/5165352
            raise AttributeError()
        return getattr(self._model, key)

    def merge(self, other):
        keys = set(self).union(other)
        empty_list = []
        return dict(
            (key, self.get(key, empty_list) + other.get(key, empty_list))
            for key
            in keys
        )

    @staticmethod
    def _from_files(word_files, image_directory):
        return _ModelBuilder(word_files, image_directory).build()


class _ModelBuilder(object):

    def __init__(self, word_files, image_directory):
        self._data_set = DataSet.from_files(
            words_files=word_files,
            image_files_directory=image_directory
        )
        self._pre_processor = pipe.pipe().pipe_line
        self._feature_extractor = characterFeatureExtraction.extract()

    def build(self):
        model = dict()
        self._data_set.pre_process(self._pre_processor)
        self._data_set.extract_features(self._feature_extractor)
        return model

    # def _pre_process(self):
    #     for _, page in self._dataset.pages():
    #         page.preprocessed_np_array = pipe.pipe().pipe_line(page.image_as_np_array)
    #
    # def _extract_features(self):
    #     for _, character in self.dataset.characters():
    #         feature_vector = characterFeatureExtraction.extract(character.preprocessed_np_array)

if __name__ == '__main__':
    pass
    # Input arguments: list of words files, directory with image files.


    # return dictionary
