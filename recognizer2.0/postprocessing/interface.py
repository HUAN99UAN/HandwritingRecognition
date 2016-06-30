class AbstractPostProcessor(object):
    """AbstractPostProcessor defines the interface for post processors."""

    def __init__(self):
        super(AbstractPostProcessor, self).__init__()
    def process(self, text):
        """
        Post process the text.
        :rtype: a string representing the new text.
        :param text: the text found by the classifier.
        """
        pass

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


