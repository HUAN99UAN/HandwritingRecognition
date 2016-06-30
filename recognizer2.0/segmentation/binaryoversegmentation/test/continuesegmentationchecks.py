import unittest
from unittest import TestCase

import numpy as np

import segmentation.binaryoversegmentation.continuesegmentationchecks as checks
from segmentation.binaryoversegmentation.segmentationimage import SegmentationImage
from segmentation.binaryoversegmentation.segmentationlines import SegmentationLines, SegmentationLine
import utils.image as imagemodule


class TestContinueOnWidthCheck(TestCase):
    def setUp(self):
        super(TestContinueOnWidthCheck, self).setUp()
        self._check = checks.ContinueOnWidthCheck(average_character_width=3, minimum_character_width=2)

    def test_continue_segmentation_1(self):
        image_size = (5, 2)
        image_array = np.array(np.random.random(image_size) * 255, dtype=np.uint8)
        image = imagemodule.Image(image_array, imagemodule.ColorMode.binary)
        segmentation_image = SegmentationImage(image, SegmentationLines([]))

        actual = self._check.continue_segmentation(segmentation_image)
        self.assertFalse(actual)

    def test_continue_segmentation_2(self):
        image_size = (5, 8)
        image_array = np.array(np.random.random(image_size) * 255, dtype=np.uint8)
        image = imagemodule.Image(image_array, imagemodule.ColorMode.binary)
        segmentation_image = SegmentationImage(image, SegmentationLines([]))

        actual = self._check.continue_segmentation(segmentation_image)
        self.assertTrue(actual)

    def test_continue_segmentation_3(self):
        image_size = (5, 4)
        image_array = np.array(np.random.random(image_size) * 255, dtype=np.uint8)
        image = imagemodule.Image(image_array, imagemodule.ColorMode.binary)
        segmentation_image = SegmentationImage(image, SegmentationLines([]))

        actual = self._check.continue_segmentation(segmentation_image)
        self.assertTrue(actual)


class TestContinueOnNumberOfForegroundPixels(TestCase):
    def setUp(self):
        super(TestContinueOnNumberOfForegroundPixels, self).setUp()
        self._check = checks.ContinueOnNumberOfForegroundPixels(minimum_number_of_foreground_pixels=4)

    def test_continue_segmentation_1(self):
        image_size = (5, 4)
        image_array = np.array(np.zeros(image_size) * 255, dtype=np.uint8)
        image = imagemodule.Image(image_array, imagemodule.ColorMode.binary)
        segmentation_image = SegmentationImage(image, SegmentationLines([]))

        actual = self._check.continue_segmentation(segmentation_image)
        self.assertFalse(actual)

    def test_continue_segmentation_2(self):
        image_size = (5, 4)
        image_array = np.array(np.ones(image_size) * 255, dtype=np.uint8)
        image = imagemodule.Image(image_array, imagemodule.ColorMode.binary)
        segmentation_image = SegmentationImage(image, SegmentationLines([]))

        actual = self._check.continue_segmentation(segmentation_image)
        self.assertTrue(actual)


class TestContinueOnSSPCheck(TestCase):
    def setUp(self):
        super(TestContinueOnSSPCheck, self).setUp()
        self._check = checks.ContinueOnSSPCheck()

    def test_continue_segmentation_1(self):
        image_size = (5, 4)
        image_array = np.array(np.random.random(image_size) * 255, dtype=np.uint8)
        image = imagemodule.Image(image_array, imagemodule.ColorMode.binary)
        segmentation_lines = SegmentationLines([SegmentationLine(x=0), SegmentationLine(x=2)])
        segmentation_image = SegmentationImage(image, segmentation_lines)

        actual = self._check.continue_segmentation(segmentation_image)
        self.assertTrue(actual)

    def test_continue_segmentation_2(self):
        image_size = (5, 4)
        image_array = np.array(np.random.random(image_size) * 255, dtype=np.uint8)
        image = imagemodule.Image(image_array, imagemodule.ColorMode.binary)
        segmentation_lines = SegmentationLines([])
        segmentation_image = SegmentationImage(image, segmentation_lines)

        actual = self._check.continue_segmentation(segmentation_image)
        self.assertFalse(actual)

if __name__ == '__main__':
    unittest.main()