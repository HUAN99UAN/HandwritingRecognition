class AbstractClassifier(object):
    """AbstractClassifier defines the interfaces for classifiers."""

    def __init__(self, model_file, **parameters):
        """
        Constructor of a Classifier.
        :param model_file: The file of the model to be used by the classifier.
        :param parameters:
        """
        super(AbstractClassifier, self).__init__()
        self._model = self._model_file_to_model(model_file)
        self._parameters = parameters

    def classify(self, feature_vector):
        """
        Method that classifies a feature vector
        :rtype: string with the text of the word image.
        :param features: 1D array-like object.
        """
        raise NotImplementedError()

    def build_model(self, xml_files, image_folder, preprocessor, feature_extractor):
        raise NotImplementedError()

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
