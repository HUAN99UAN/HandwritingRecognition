import unittest
from unittest import TestCase

import numpy as np

from utils.image import Image, ColorMode
from featureExtraction.crossings import Crossings


class TestCrossings(TestCase):

    def setUp(self):
        super(TestCrossings, self).setUp()
        image_array = np.asarray(np.array([[0, 0, 1, 1], [1, 0, 0, 1], [0, 0, 1, 0], [1, 0, 1, 1], [0, 0, 1, 1]]) * 255, np.uint8)
        self.image = Image(image_array, color_mode=ColorMode.binary)

    def test_extract(self):
        number_of_vertical_features, number_of_horizontal_features = 4, 4
        extractor = Crossings(
            number_of_horizontal_features=number_of_horizontal_features,
            number_of_vertical_features=number_of_vertical_features
        )
        actual_feature_vector = extractor.extract(self.image)
        expected_feature_vector = np.array([1, 2, 2, 2, 1, 4, 0, 2, 2])
        np.testing.assert_array_equal(actual_feature_vector, expected_feature_vector)

    def test__scale_image(self):
        number_of_features = 4
        extractor = Crossings()
        actual_image = extractor._scale_image(self.image, number_of_features)
        expected_height = 4
        expected_color_mode = ColorMode.binary
        self.assertEqual(actual_image.height, expected_height)
        self.assertEqual(actual_image.color_mode, expected_color_mode)

    def test__scale_image_2(self):
        number_of_features = 8
        extractor = Crossings()
        actual_image = extractor._scale_image(self.image, number_of_features)
        expected_height = 8
        expected_color_mode = ColorMode.binary
        self.assertEqual(actual_image.height, expected_height)
        self.assertEqual(actual_image.color_mode, expected_color_mode)

    def test__compute_crossing_features_horizontal(self):
        axis, number_of_features = 1, 4
        extractor = Crossings()
        actual_features = extractor._count_crossings(image=self.image, number_of_features=number_of_features, axis=axis)
        expected_features = np.array([1, 2, 2, 2, 1], dtype=np.uint8)
        np.testing.assert_array_equal(actual_features, expected_features)

    def test__compute_crossing_features_vertical(self):
        axis, number_of_features = 0, 4
        extractor = Crossings()
        actual_features = extractor._count_crossings(image=self.image, number_of_features=number_of_features, axis=axis)
        expected_features = np.array([4, 0, 2, 2], dtype=np.uint8)
        np.testing.assert_array_equal(actual_features, expected_features)


if __name__ == '__main__':
    unittest.main()