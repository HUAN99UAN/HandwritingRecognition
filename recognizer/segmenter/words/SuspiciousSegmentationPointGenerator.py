from statistics import mode

import numpy as np

from utils.lists import flatten_one_level
from utils.decorators import lazy_property
from utils.shapes import HorizontalLine


class SSPGenerator:
    """Class that generates the suspicious segmentation points

    Args:
        image (PIL.Image): A gray scale image in which we determine the suspicious segmentation points.
        white_threshold: The white threshold to be used, gray scales lower than this value are foreground, gray
            values greater than this value are background. Defaults to default_parameters['white_threshold'].
    """
    def __init__(self, image, white_threshold, **kwargs):
        self._image = image
        self._white_threshold = white_threshold

        self._stroke_width = _StrokeWidthComputer(foreground=self.image_foreground).compute()
        self._base_line = BaseLines.compute(image=self.image_foreground)
        self._segment_criteria = self._stroke_width * 2
    @property
    def base_lines(self):
        return self._base_lines

    @property
    def _segment_criterion(self):
        return self._stroke_width * 2

    @lazy_property
    def image_foreground(self):
        return self.image_array < self._white_threshold

    @lazy_property
    def image_array(self):
        return np.array(self._image)

    @lazy_property
    def body_region(self):
        row_indices_body = list(range(
            self._base_lines.high_base_line_y,
            self._base_lines.low_base_line_y + 1
        ))
        return self.image_array.take(row_indices_body, axis=0)

    @lazy_property
    def suspicious_segmentation_points(self):
    def paint_base_lines(self, image=None):
        image = image or self._image
        return self._base_line.paint(image)


class SuspiciousSegmentationPoint:

    def __init__(self, x):
        self._x = x


class BaseLines:
    """Class to represent the low and the high baseline of a word or line of text."""

    def __init__(self, high_base_line, low_base_line, left_x, right_x):
        """The constructor of the BaseLines class.

        Args:
            high_base_line: The index into a column the baseline lying on the top of the letters
            low_base_line: The index into a column of the baseline touchign the bottom of the letters.
        """
        self._high_base_line = HorizontalLine(left_x, right_x, high_base_line)
        self._low_base_line = HorizontalLine(left_x, right_x, low_base_line)

    @property
    def low_base_line_y(self):
        return self._low_base_line.y

    @property
    def high_base_line_y(self):
        return self._high_base_line.y

    @staticmethod
    def compute(image):
        return _BaseLineComputer(foreground=image).compute()

    def paint(self, image):
        self._high_base_line.paint_on(image)
        self._low_base_line.paint_on(image)
        return image


class _BaseLineComputer:
    """Class to compute the thickness of the pen stroke of a word in an image."""

    def __init__(self, foreground):
        """The constructor of the _BaseLineComputer class.

        Args:
            foreground: A 2D bool array with the foreground pixels set to true
        """
        self._foreground = foreground

    def _base_lines(self):
        (high_column_base_lines, low_column_base_lines) = (list(), list())
        for column in self._foreground.T:
            indices = np.where(column)
            if indices[0].size is not 0:
                high_column_base_lines.append(np.min(indices))
                low_column_base_lines.append(np.max(indices))
        return mode(low_column_base_lines), mode(high_column_base_lines)

    def compute(self):
        (low_base_line, high_base_line) = self._base_lines()
        return BaseLines(
            low_base_line=low_base_line, high_base_line=high_base_line,
            left_x=0, right_x=self._foreground.shape[1]
        )


class _StrokeWidthComputer:
    """Class to compute the thickness of the pen stroke of a word in an image."""

    def __init__(self, foreground):
        """The constructor of the StrokeWidthComputer class.

        Args:
            foreground: A 2D bool array with the foreground pixels set to true
        """
        self._foreground = foreground

    def compute(self):
        sequences = self._find_continuous_foreground_sequences()
        return mode(sequences)

    @staticmethod
    def _runs_of_ones(bits):
        # source http://stackoverflow.com/a/1066838
        # make sure all runs of ones are well-bounded
        bounded = np.hstack(([0], bits, [0]))
        # get 1 at run starts and -1 at run ends
        difs = np.diff(bounded)
        run_starts, = np.where(difs > 0)
        run_ends, = np.where(difs < 0)
        return list(run_ends - run_starts)

    def _find_continuous_foreground_sequences(self):
        sequences = list()
        sequences.extend(self._vertical_sequence_lengths())
        sequences.extend(self._horizontal_sequence_lengths())
        return sequences

    def _vertical_sequence_lengths(self):
        return flatten_one_level(
            [_StrokeWidthComputer._runs_of_ones(sequence)
             for sequence
             in self._foreground
             ]
        )

    def _horizontal_sequence_lengths(self):
        return flatten_one_level(
            [_StrokeWidthComputer._runs_of_ones(sequence)
             for sequence
             in np.transpose(self._foreground)
             ]
        )
