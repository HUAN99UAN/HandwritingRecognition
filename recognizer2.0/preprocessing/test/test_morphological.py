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


class TestReconstructionByDilation(TestCase):
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
        reconstruction_by_dilation = ReconstructionByDilation(
            mask_image=self.mask,
            structuring_element=self.structuring_element
        )
        actual = reconstruction_by_dilation.apply(self.marker)
        expected = self.mask
        np.testing.assert_array_equal(actual, expected)


class TestReconstructionByErosion(TestCase):
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
        reconstruction_by_erosion = ReconstructionByErosion(
            mask_image=self.mask,
            structuring_element=self.structuring_element
        )
        actual = reconstruction_by_erosion.apply(self.marker)
        expected = self.mask
        np.testing.assert_array_equal(actual, expected)


class TestReconstructionByOpening(TestCase):
    def setUp(self):
        self.image = np.zeros((9, 10))
        self.image[5:10, 0:4] = 1
        self.image[1, 1] = self.image[7, 3] = 1
        self.image = Image(self.image, color_mode=ColorMode.binary)

        self.structuring_element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def test_apply(self):
        reconstruction_by_opening = ReconstructionByOpening(structuring_element=self.structuring_element, iterations=1)
        actual = reconstruction_by_opening.apply(self.image)

        expected = np.zeros((9, 10))
        expected[5:10, 0:4] = 1
        expected = Image(expected, color_mode = ColorMode.binary)

        np.testing.assert_array_equal(actual, expected)

    def test_apply_2(self):
        reconstruction_by_opening = ReconstructionByOpening(structuring_element=self.structuring_element, iterations=2)
        actual = reconstruction_by_opening.apply(self.image)

        expected = np.zeros((9,10))
        expected[5:10, 0:4] = 1
        expected = Image(expected, color_mode=ColorMode.binary)

        np.testing.assert_array_equal(actual, expected)


class TestReconstructionByClosing(TestCase):
    def setUp(self):
        self.image = np.zeros((9, 10))
        self.image[1:4, 1:5] = 1
        self.image[2, 2:4] = 0
        self.image = Image(self.image, color_mode=ColorMode.binary)

        self.structuring_element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def test_apply(self):
        raise NotImplementedError("Blurgh, I'll have to write this test eventually.")

if __name__ == '__main__':
    unittest.main()
