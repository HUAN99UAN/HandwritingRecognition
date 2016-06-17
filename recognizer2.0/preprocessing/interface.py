class AbstractFilter(object):
    """AbstractFilter defines the interfaces for preprocessing filters."""

    def __init__(self, **parameters):
        """
        :param parameters: A dictionary with the parameters for this filter.
        """
        super(AbstractFilter, self).__init__()
        self._parameters = parameters

    def apply(self, image):
        """
        Apply this filter to the image.
        :param image: The image to filter, should be arraylike.
        :return: The filtered image.
        """
        pass

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class AbstractFilterBank(object):
    """AbstractFilterBank defines the interfaces for pre-processing filter banks.."""

    def __init__(self, filters):
        """
        :param filters: A list of Filter objects, the filters are applied in the order of this list.
        """
        super(AbstractFilterBank, self).__init__()
        self._filters = filters

    def apply(self, image):
        """
        Apply this filter bank to the image.
        :param image: The image to filter, should be arraylike.
        :return: The filtered image.
        """
        for pre_processing_filter in self._filters:
            image = pre_processing_filter.apply(image)
        return image

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)