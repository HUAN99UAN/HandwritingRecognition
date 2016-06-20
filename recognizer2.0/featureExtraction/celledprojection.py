import featureExtraction.interface as interface
from utils.things import Size

class CelledProjection(interface.AbstractFeatureExtractor):
    """Feature extraction with celled proection.

    Source: Hossain, M. Zahid, M. Ashraful Amin, and Hong Yan. "Rapid feature extraction for optical character
    recognition."
    """

    _default_extraction_size = Size(width=128, height = 128)

    def __init__(self, extraction_size=_default_extraction_size):
        super(CelledProjection, self).__init__()
        self._extraction_size = extraction_size

    def extract(self, image):
        raise NotImplementedError()
        # Resize image to self.extraction_size
        # Invert image
        # Comput crossing feature

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
