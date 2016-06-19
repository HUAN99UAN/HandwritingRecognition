import unittest
from unittest import TestCase

import numpy as np
import cv2

from utils.image import Image, ColorMode
from preprocessing.morphological import *


class TestGeodesicDilation(TestCase):
    def setUp(self):
        self.marker = np.zeros((9, 10))
        self.marker[2, 2] = 1
        self.marker = Image(self.marker, color_mode=ColorMode.binary)

        self.structuring_element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        self.mask = np.zeros((9, 10))
        self.mask[2, 2] = self.mask[3, 2] = self.mask[3:8, 3] = 1
        self.mask[7, 3:6] = self.mask[5, 3:6] = self.mask[6, 5] = 1
        self.mask = Image(self.mask, color_mode=ColorMode.binary)

    def test_apply(self):
        geodesic_dilation = GeodesicDilation(
            iterations=1,
            mask_image=self.mask,
            structuring_element=self.structuring_element
        )
        actual = geodesic_dilation.apply(self.marker)
        expected = np.zeros((9, 10))
        expected[2, 2] = expected[3, 2] = expected[3, 3] = 1
        np.testing.assert_array_equal(actual, expected)

    def test_apply_2(self):
        geodesic_dilation = GeodesicDilation(
            iterations=2,
            mask_image=self.mask,
            structuring_element=self.structuring_element
        )
        actual = geodesic_dilation.apply(self.marker)
        expected = np.zeros((9, 10))
        expected[2, 2] = expected[3, 2] = expected[3, 3] = expected[4, 3] = 1
        np.testing.assert_array_equal(actual, expected)


class TestGeodesicErosion(TestCase):
    def setUp(self):
        self.marker = np.zeros((9, 10))
        self.marker[1:5, 1:7] = 1
        self.marker[1, 6] = 0
        self.marker[4, 1:3] = 0
        self.marker = Image(self.marker, color_mode=ColorMode.binary)

        self.structuring_element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        self.mask = np.zeros((9, 10))
        self.mask[2, 2] = self.mask[3, 2] = self.mask[3:8, 3] = 1
        self.mask[7, 3:6] = self.mask[5, 3:6] = self.mask[6, 5] = 1
        self.mask = Image(self.mask, color_mode=ColorMode.binary)

    def test_apply(self):
        geodesic_erosion= GeodesicErosion(
            iterations=1,
            mask_image=self.mask,
            structuring_element=self.structuring_element
        )
        actual = geodesic_erosion.apply(self.marker)
        expected = np.zeros((9, 10))
        expected[2:8, 2:6] = 1
        expected[2, 5] = expected[4,4] = expected[4, 5] = expected[6, 4] = 0
        expected[4:8, 2] = 0
        np.testing.assert_array_equal(actual, expected)

    def test_apply_2(self):
        geodesic_erosion= GeodesicErosion(
            iterations=1,
            mask_image=self.mask,
            structuring_element=self.structuring_element
        )
        actual = geodesic_erosion.apply(self.marker)
        expected = np.zeros((9, 10))
        expected[2:8, 2:6] = 1
        expected[2, 5] = expected[4,4] = expected[4, 5] = expected[6, 4] = 0
        expected[4:8, 2] = 0
        np.testing.assert_array_equal(actual, expected)


if __name__ == '__main__':
    unittest.main()
