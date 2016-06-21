import interface
from preprocessing import luminosity, otsu, morphological


class OriginalPreProcessor(interface.AbstractFilterBank):
    """The preprocessor as used in the first version of our application."""

    def __init__(self, filters=[]):
        filters = [
            luminosity.LuminosityNormalization(),
            otsu.OtsuMethod(),
            morphological.Closing(),
            morphological.ReconstructionByOpening()
        ]
        super(OriginalPreProcessor, self).__init__(filters=filters)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
