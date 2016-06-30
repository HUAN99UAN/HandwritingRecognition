class AbstractClassifier(object):
    """AbstractClassifier defines the interfaces for classifiers."""

    def __init__(self):
        super(AbstractClassifier, self).__init__()

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