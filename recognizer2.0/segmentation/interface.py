class AbstractSegmenter(object):
    """AbstractClassifier defines the interfaces for classifiers."""

    def __init__(self, **parameters):
        super(AbstractSegmenter, self).__init__()
        self._parameters = parameters

    def segment(self, image):
        """
        :param image: the image to segment
        :rtype: List of subimages of image.
        """
        pass

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
