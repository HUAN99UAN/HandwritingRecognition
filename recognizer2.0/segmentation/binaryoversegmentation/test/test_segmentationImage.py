import unittest
from unittest import TestCase
import copy

import numpy as np


from segmentation.binaryoversegmentation.segmentationimage import SegmentationImage
from segmentation.binaryoversegmentation.segmentationlines import SegmentationLines
from utils.image import Image, ColorMode
from utils.things import BoundingBox


class TestSegmentationImage(TestCase):
    def setUp(self):
        image_array = np.array([
            [0, 0, 1, 0, 1, 1],
            [1, 0, 0, 1, 0, 0],
            [1, 1, 1, 0, 1, 1],
        ], dtype=np.uint8) * 255
        image = Image(image_array, ColorMode.binary)
        segmentation_lines = SegmentationLines.from_x_coordinates([1, 4])
        self.character_validators = [1, 2, 3]
        self.continue_segmentation_checks = [2, 3, 4]
        self.image_splitter = 'ImageSplitter'
        self.image = SegmentationImage(image, segmentation_lines,
                                       self.character_validators,
                                       self.continue_segmentation_checks,
                                       self.image_splitter)

    def test_sub_image_1(self):
        # Index out of range, should give IndexError
        bounding_box = BoundingBox(top=0, bottom=2, left=-1, right=5)
        with self.assertRaises(IndexError):
            self.image.sub_image(bounding_box)

    def test_sub_image_2(self):
        # Index out of range, should give original image.
        bounding_box = BoundingBox(top=-1, bottom=2, left=0, right=5)
        with self.assertRaises(IndexError):
            self.image.sub_image(bounding_box)

    def test_sub_image_3(self):
        # Index out of range, should give original image
        bounding_box = BoundingBox(top=0, bottom=self.image.height, left=0, right=5)
        with self.assertRaises(IndexError):
            self.image.sub_image(bounding_box)

    def test_sub_image_4(self):
        # Index out of range, should give original image
        bounding_box = BoundingBox(top=0, bottom=2, left=0, right=self.image.width)
        with self.assertRaises(IndexError):
            self.image.sub_image(bounding_box)

    def test_sub_image_5(self):
        # Bounding box has image size, should give original image.
        bounding_box = BoundingBox(top=0, bottom=2, left=0, right=5)
        actual_image = self.image.sub_image(bounding_box)
        expected_image = self.image
        np.testing.assert_array_equal(actual_image, expected_image)
        self.assertEqual(actual_image._segmentation_lines, expected_image._segmentation_lines)
        self.assertItemsEqual(actual_image._character_validators, expected_image._character_validators)
        self.assertItemsEqual(actual_image._continue_segmentation_checks, expected_image._continue_segmentation_checks)
        self.assertItemsEqual(actual_image._image_splitter, expected_image._image_splitter)

    def test_sub_image_6(self):
        # Take the left half of the image
        bounding_box = BoundingBox(top=0, bottom=2, left=0, right=2)
        actual_image = self.image.sub_image(bounding_box)

        image_array = np.array([
            [0, 0, 1],
            [1, 0, 0],
            [1, 1, 1],
        ], dtype=np.uint8) * 255
        image = Image(image_array, ColorMode.binary)
        segmentation_lines = SegmentationLines.from_x_coordinates([1])
        expected_image = SegmentationImage(image, segmentation_lines,
                                           self.character_validators,
                                           self.continue_segmentation_checks,
                                           self.image_splitter)
        np.testing.assert_array_equal(actual_image, expected_image)
        self.assertEqual(actual_image._segmentation_lines, expected_image._segmentation_lines)
        self.assertItemsEqual(actual_image._character_validators, expected_image._character_validators)
        self.assertItemsEqual(actual_image._continue_segmentation_checks, expected_image._continue_segmentation_checks)
        self.assertItemsEqual(actual_image._image_splitter, expected_image._image_splitter)

    def test_sub_image_7(self):
        # Take the right half of the image
        bounding_box = BoundingBox(top=0, bottom=2, left=2, right=5)
        actual_image = self.image.sub_image(bounding_box)

        image_array = np.array([
            [1, 0, 1, 1],
            [0, 1, 0, 0],
            [1, 0, 1, 1],
        ], dtype=np.uint8) * 255
        image = Image(image_array, ColorMode.binary)
        segmentation_lines = SegmentationLines.from_x_coordinates([2])
        expected_image = SegmentationImage(image, segmentation_lines,
                                           self.character_validators,
                                           self.continue_segmentation_checks,
                                           self.image_splitter)
        np.testing.assert_array_equal(actual_image, expected_image)
        self.assertEqual(actual_image._segmentation_lines, expected_image._segmentation_lines)
        self.assertItemsEqual(actual_image._character_validators, expected_image._character_validators)
        self.assertItemsEqual(actual_image._continue_segmentation_checks, expected_image._continue_segmentation_checks)
        self.assertItemsEqual(actual_image._image_splitter, expected_image._image_splitter)

    def test_sub_image_8(self):
        # Take the top half of the image
        bounding_box = BoundingBox(top=0, bottom=1, left=0, right=5)
        actual_image = self.image.sub_image(bounding_box)

        image_array = np.array([
            [0, 0, 1, 0, 1, 1],
            [1, 0, 0, 1, 0, 0],
        ], dtype=np.uint8) * 255
        image = Image(image_array, ColorMode.binary)
        segmentation_lines = SegmentationLines.from_x_coordinates([1, 4])
        expected_image = SegmentationImage(image, segmentation_lines,
                                           self.character_validators,
                                           self.continue_segmentation_checks,
                                           self.image_splitter)
        np.testing.assert_array_equal(actual_image, expected_image)
        self.assertEqual(actual_image._segmentation_lines, expected_image._segmentation_lines)
        self.assertItemsEqual(actual_image._character_validators, expected_image._character_validators)
        self.assertItemsEqual(actual_image._continue_segmentation_checks, expected_image._continue_segmentation_checks)
        self.assertItemsEqual(actual_image._image_splitter, expected_image._image_splitter)

    def test_sub_image_9(self):
        # Take the bottom half of the image
        bounding_box = BoundingBox(top=1, bottom=2, left=0, right=5)
        actual_image = self.image.sub_image(bounding_box)

        image_array = np.array([
            [1, 0, 0, 1, 0, 0],
            [1, 1, 1, 0, 1, 1],
        ], dtype=np.uint8) * 255
        image = Image(image_array, ColorMode.binary)
        segmentation_lines = SegmentationLines.from_x_coordinates([1, 4])
        expected_image = SegmentationImage(image, segmentation_lines,
                                           self.character_validators,
                                           self.continue_segmentation_checks,
                                           self.image_splitter)

        np.testing.assert_array_equal(actual_image, expected_image)
        self.assertEqual(actual_image._segmentation_lines, expected_image._segmentation_lines)
        self.assertItemsEqual(actual_image._character_validators, expected_image._character_validators)
        self.assertItemsEqual(actual_image._continue_segmentation_checks, expected_image._continue_segmentation_checks)
        self.assertItemsEqual(actual_image._image_splitter, expected_image._image_splitter)

    def test_concat_with(self):
        left_lines = SegmentationLines.from_x_coordinates([0, 1])
        left_pixels = np.zeros((3, 2))
        left_pixels[0, 1] = left_pixels[1, 1] = left_pixels[2, 0] = left_pixels[2, 1] = 1
        left_image = Image(left_pixels, color_mode=ColorMode.binary)
        left_image = SegmentationImage(left_image, left_lines,
                                           self.character_validators,
                                           self.continue_segmentation_checks,
                                           self.image_splitter)

        right_lines = SegmentationLines.from_x_coordinates([0, 1])
        right_pixels = np.zeros((3, 2))
        right_pixels[0, 1] = right_pixels[1, 0] = right_pixels[1, 1] = 1
        right_image = Image(right_pixels, color_mode=ColorMode.binary)
        right_image = SegmentationImage(right_image, right_lines,
                                       self.character_validators,
                                       self.continue_segmentation_checks,
                                       self.image_splitter)

        expected_pixels = np.zeros((3, 4))
        expected_lines = SegmentationLines.from_x_coordinates([0, 1, 2, 3])
        expected_pixels[0, 1] = expected_pixels[1, 1] = expected_pixels[2, 0] = expected_pixels[2, 1] = 1
        expected_pixels[0, 3] = expected_pixels[1, 2] = expected_pixels[1, 3] = 1
        expected = Image(expected_pixels, color_mode=ColorMode.binary)
        expected_image = SegmentationImage(expected, expected_lines,
                                       self.character_validators,
                                       self.continue_segmentation_checks,
                                       self.image_splitter)

        actual_image = left_image.concat_with(right_image)
        np.testing.assert_array_equal(actual_image, expected_image)
        self.assertEqual(actual_image._segmentation_lines, expected_image._segmentation_lines)
        self.assertItemsEqual(actual_image._character_validators, expected_image._character_validators)
        self.assertItemsEqual(actual_image._continue_segmentation_checks, expected_image._continue_segmentation_checks)
        self.assertItemsEqual(actual_image._image_splitter, expected_image._image_splitter)

    def test_show(self):
        expected = copy.deepcopy(self.image)
        self.image.show(color=(0, 0, 0), window_name='Actual', wait_key=1)
        np.testing.assert_array_equal(self.image, expected)


if __name__ == '__main__':
    unittest.main()
