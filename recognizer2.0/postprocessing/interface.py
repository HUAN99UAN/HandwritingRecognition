class AbstractPostProcessor(object):
    """AbstractPostProcessor defines the interface for post processors."""

    def __init__(self, model_file, parameters):
        super(AbstractPostProcessor, self).__init__()
        self._parameters = parameters
        self._model = self._model_file_to_model(model_file)

    def process(self, text):
        """
        Post process the text.
        :rtype: a string representing the new text.
        :param text: the text found by the classifier.
        """
        pass

    @classmethod
    def _model_file_to_model(cls, model_file):
        pass

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
