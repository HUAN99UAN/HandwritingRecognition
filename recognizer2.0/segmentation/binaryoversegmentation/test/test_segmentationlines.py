import unittest
from unittest import TestCase

from segmentation.binaryoversegmentation.segmentationlines import SegmentationLine, SegmentationLines


class TestSegmentationLine(TestCase):
    def setUp(self):
        self.line = SegmentationLine(x=5)

    def test_shift_horizontally_positive(self):
        distance = 4
        actual = self.line.shift_horizontally(distance)
        expected = SegmentationLine(x=9)
        self.assertEqual(actual, expected)

    def test_shift_horizontally_negative(self):
        distance = -4
        actual = self.line.shift_horizontally(distance)
        expected = SegmentationLine(x=1)
        self.assertEqual(actual, expected)

from unittest import TestCase


class TestSegmentationLines(TestCase):
    def setUp(self):
        self.lines = SegmentationLines.from_x_coordinates([3, 5])

    def test_shift_horizontally_positive(self):
        distance = 4
        actual = self.lines.shift_horizontally(distance)
        expected = SegmentationLines.from_x_coordinates([7, 9])
        self.assertEqual(actual, expected)

    def test_shift_horizontally_negative(self):
        distance = -4
        expected = SegmentationLines.from_x_coordinates([-1, 1])
        actual = self.lines.shift_horizontally(distance)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()