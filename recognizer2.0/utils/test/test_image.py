import unittest
from unittest import TestCase

import numpy as np

from utils.image import Image, ColorMode
from utils.things import BoundingBox


class TestImage(TestCase):

    def setUp(self):
        self.image = Image(np.asarray(np.random.rand(20, 5) * 255, np.uint8), color_mode=ColorMode.gray)

    def test_resize_0(self):
        width = 80
        resized_image = self.image.resize(width=width)
        expected_width, expected_height = 80, 320
        self.assertEqual(resized_image.width, expected_width)
        self.assertEqual(resized_image.height, expected_height)

    def test_resize_1(self):
        height = 80
        resized_image = self.image.resize(height=height)
        expected_width, expected_height = 20, 80
        self.assertEqual(resized_image.width, expected_width)
        self.assertEqual(resized_image.height, expected_height)

    def test_resize_2(self):
        width, height = 80, 20
        resized_image = self.image.resize(width=width, height=height)
        expected_width, expected_height = 5, 20
        self.assertEqual(resized_image.width, expected_width)
        self.assertEqual(resized_image.height, expected_height)

    def test_resize_3(self):
        width, height = 80, 20
        resized_image = self.image.resize(width=width, height=height, keepaspect_ratio=False)
        expected_width, expected_height = 80, 20
        self.assertEqual(resized_image.width, expected_width)
        self.assertEqual(resized_image.height, expected_height)

    def test_resize_4(self):
        width, height = 80, 20
        resized_image = self.image.resize(width=width, height=height, keepaspect_ratio=True)
        expected_width, expected_height = 5, 20
        self.assertEqual(resized_image.width, expected_width)
        self.assertEqual(resized_image.height, expected_height)

    def test_resize_5(self):
        width, height = -5, 10
        with self.assertRaises(KeyError):
            self.image.resize(width=width, height=height, keepaspect_ratio=True)

    def test_resize_6(self):
        width, height = 5, -10
        with self.assertRaises(KeyError):
            self.image.resize(width=width, height=height, keepaspect_ratio=True)

    def test_resize_7(self):
        with self.assertRaises(TypeError):
            self.image.resize()

class TestSubImage(TestCase):

    def test_no_white_space(self):
        image_array = np.array(np.zeros((5,5)), dtype=np.uint8)
        image = Image(image_array, ColorMode.binary)
        bounding_box = BoundingBox(top=0, bottom=2, left=0, right=2)

        actual = image.sub_image(bounding_box, remove_white_borders=True)
        expected = Image(
            np.array(np.zeros((3, 3)), dtype=np.uint8),
            ColorMode.binary
        )
        np.testing.assert_array_equal(actual, expected)

    def test_left_white_space(self):
        image_array = np.array([
            [1, 0, 0, 1],
            [1, 0, 1, 0],
            [1, 1, 1, 0]
        ], dtype=np.uint8) * 255
        image = Image(image_array, ColorMode.binary)
        bounding_box = BoundingBox(top=0, bottom=2, left=0, right=2)

        actual = image.sub_image(bounding_box, remove_white_borders=True)
        expected = Image(
            np.array([
                [0, 0],
                [0, 1],
                [1, 1]
            ], dtype=np.uint8) * 255,
            ColorMode.binary
        )
        np.testing.assert_array_equal(actual, expected)

    def test_right_white_space(self):
        image_array = np.array([
            [1, 0, 1, 0, 1],
            [0, 1, 0, 1, 1],
            [1, 1, 1, 0, 1],
        ], dtype=np.uint8) * 255
        image = Image(image_array, ColorMode.binary)
        bounding_box = BoundingBox(top=0, bottom=2, left=2, right=4)

        actual = image.sub_image(bounding_box, remove_white_borders=True)
        expected = Image(
            np.array([
                [1, 0],
                [0, 1],
                [1, 0],
            ], dtype=np.uint8) * 255,
            ColorMode.binary
        )
        np.testing.assert_array_equal(actual, expected)

    def test_top_white_space(self):
        image_array = np.array([
            [1, 1, 1, 1, 1],
            [0, 1, 0, 1, 1],
            [1, 1, 1, 0, 1],
        ], dtype=np.uint8) * 255
        image = Image(image_array, ColorMode.binary)
        bounding_box = BoundingBox(top=0, bottom=2, left=0, right=4)

        actual = image.sub_image(bounding_box, remove_white_borders=True)
        expected = Image(
            np.array([
                [0, 1, 0, 1, 1],
                [1, 1, 1, 0, 1],
            ], dtype=np.uint8) * 255,
            ColorMode.binary
        )
        np.testing.assert_array_equal(actual, expected)

    def test_bottom_white_space(self):
        image_array = np.array([
            [1, 1, 1, 0, 1],
            [0, 1, 0, 1, 1],
            [1, 1, 1, 1, 1],
        ], dtype=np.uint8) * 255
        image = Image(image_array, ColorMode.binary)
        bounding_box = BoundingBox(top=0, bottom=2, left=0, right=4)

        expected = Image(
            np.array([
                [1, 1, 1, 0, 1],
                [0, 1, 0, 1, 1],
            ], dtype=np.uint8) * 255,
            ColorMode.binary
        )
        actual = image.sub_image(bounding_box, remove_white_borders=True)
        np.testing.assert_array_equal(actual, expected)

    def test_white_space_on_all_sides(self):
        image_array = np.array([
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
        ], dtype=np.uint8) * 255
        image = Image(image_array, ColorMode.binary)
        bounding_box = BoundingBox(top=0, bottom=2, left=0, right=4)

        expected = Image(
            np.array([
                [1, 0, 0, 0, 1],
            ], dtype=np.uint8) * 255,
            ColorMode.binary
        )
        actual = image.sub_image(bounding_box, remove_white_borders=True)
        np.testing.assert_array_equal(actual, expected)

    def test_only_white_space(self):
        image_array = np.array(np.ones((5,5)), dtype=np.uint8) * 255
        image = Image(image_array, ColorMode.binary)
        bounding_box = BoundingBox(top=0, bottom=4, left=0, right=4)

        actual = image.sub_image(bounding_box, remove_white_borders=True)
        self.assertIsNone(actual)


if __name__ == '__main__':
    unittest.main()