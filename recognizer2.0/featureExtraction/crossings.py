import featureExtraction.interface as interface
from preprocessing.colorspaces import ToBinary

import numpy as np


class Crossings(interface.AbstractFeatureExtractor):
    """Feature extraction

    Source: Section 2.1 in Hossain, M. Zahid, M. Ashraful Amin, and Hong Yan. "Rapid feature extraction for optical
    character recognition."
    """

    _default_number_of_vertical_features = 64
    _default_number_of_horizontal_features = 64

    def __init__(self,
                 number_of_vertical_features=_default_number_of_vertical_features,
                 number_of_horizontal_features=_default_number_of_horizontal_features):
        super(Crossings, self).__init__()
        self._number_of_vertical_features = number_of_vertical_features
        self._number_of_horizontal_features = number_of_horizontal_features

    @property
    def number_of_features(self):
        return self._number_of_horizontal_features + self._number_of_vertical_features

    def extract(self, image):
        feature_vector_horizontal = self._count_crossings(
            image, self._number_of_horizontal_features, axis=1
        )
        feature_vector_vertical= self._count_crossings(
            image, self._number_of_vertical_features, axis=0
        )
        return np.asarray(np.hstack((feature_vector_horizontal, feature_vector_vertical)), dtype=np.float)

    @classmethod
    def _count_crossings(self, image, number_of_features, axis):
        if axis == 1:
            scaled_image = ToBinary().apply(image.resize(height=number_of_features))
        if axis == 0:
            scaled_image = ToBinary().apply(image.resize(width=number_of_features))
        differences = np.diff(scaled_image, axis=axis)
        differences[differences != 0] = 1
        return np.sum(differences, axis=axis)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
