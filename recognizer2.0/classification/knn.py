import interface


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

    def __init__(self):
        pass

    @staticmethod
    def read_from_file(model_file):
        raise NotImplementedError()

    def build(self, xml_files, image_folder, preprocessor, feature_extractor):
        _ModelBuilder(xml_files, image_folder, preprocessor, feature_extractor).build()

    def to_file(self, output_file):
        raise NotImplementedError()


class _ModelBuilder(object):

    def __init__(self, xml_files, image_folder, preprocessor, feature_extractor):
        self._xml_files = xml_files
        self._image_folder = image_folder
        self._preprocessor = preprocessor
        self._feature_extractor = feature_extractor

    def build(self):
        raise NotImplementedError()
