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

    @staticmethod
    def _concat(matrix):
        return matrix.ravel()

    @staticmethod
    def _invert_image(img):
        return (img == 0).astype(int)
