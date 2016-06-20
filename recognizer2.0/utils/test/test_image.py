import unittest
from unittest import TestCase

import numpy as np

from utils.image import Image, ColorMode
from utils.things import Size


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

if __name__ == '__main__':
    unittest.main()