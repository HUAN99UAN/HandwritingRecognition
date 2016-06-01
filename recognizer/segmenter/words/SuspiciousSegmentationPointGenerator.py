from statistics import mode

import numpy as np

from utils.lists import flatten_one_level
from utils.functionArguments import kwargs_was_valid


class SuspiciousSegmentationPointGenerator:
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
        self._base_line = BaseLine.compute(image=self.image_foreground)

    @property
    def image_foreground(self):
        return np.array(self._image) < self._white_threshold


class SuspiciousSegmentationPoint:

     def __init__(self, x):
        self._x = x


class BaseLine:
    """Class to represent the low and the high baseline of a word or line of text."""

    def __init__(self, _high_base_line, _low_base_line):
        """The constructor of the BaseLine class.

        Args:
            high_base_line: The index into a column the baseline lying on the top of the letters
            low_base_line: The index into a column of the baseline touchign the bottom of the letters.
        """
        self._high_base_line = _high_base_line
        self._low_base_line = _low_base_line

    @property
    def low_base_line(self):
        return self._low_base_line

    @property
    def high_base_line(self):
        return self._high_base_line

    @staticmethod
    def compute(image):
        return _BaseLineComputer(foreground=image).compute()


class _BaseLineComputer:
    """Class to compute the thickness of the pen stroke of a word in an image."""

    def __init__(self, foreground, **parameters):
        """The constructor of the _BaseLineComputer class.

        Args:
            foreground: A 2D bool array with the foreground pixels set to true
        """
        self._foreground = foreground

    def _base_lines(self):
        (high_column_base_lines, low_column_base_lines) = (list(), list())
        for column in np.transpose(self._foreground):
            indices = np.where(column)
            high_column_base_lines.append(np.min(indices))
            low_column_base_lines.append(np.max(indices))
        return mode(low_column_base_lines), mode(high_column_base_lines)

    def compute(self):
        (low_base_line, high_base_line) = self._base_lines()
        return BaseLine(_low_base_line=low_base_line, _high_base_line=high_base_line)


class _StrokeWidthComputer:
    """Class to compute the thickness of the pen stroke of a word in an image."""

    def __init__(self, foreground):
        """The constructor of the StrokeWidthComputer class.

        Args:
            foreground: A 2D bool array with the foreground pixels set to true
        """
        self._foreground = foreground

    def compute(self):
        sequences = self._compute_continuous_foreground_sequences()
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

    def _compute_continuous_foreground_sequences(self):
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
