class AbstractFeatureExtractor(object):
    """AbstractFeatureExtractor defines the interface for feature extractors."""

    def __init__(self, **parameters):
        super(AbstractFeatureExtractor, self).__init__()
        self._parameters = parameters

    def extract(self, image):
        """
        Extract a feature vector from image.
        :rtype: 1D array-like object
        :param image: array-like representation of an image.
        """
        pass

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
