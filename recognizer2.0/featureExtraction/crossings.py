import featureExtraction.interface as interface
from utils.things import Size


class Crossings(interface.AbstractFeatureExtractor):
    """Feature extraction

    Source: Section 2.1 in Hossain, M. Zahid, M. Ashraful Amin, and Hong Yan. "Rapid feature extraction for optical
    character recognition."
    """

    _default_number_of_features = 128

    def __init__(self, number_of_features=_default_number_of_features):
        super(Crossings, self).__init__()
        self._number_of_features = number_of_features

    def extract(self, image):
        resized_image = image.resize(width=self._number_of_features)
        # Resize image to self.extraction_size
        # Invert image
        # Comput crossing feature

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
