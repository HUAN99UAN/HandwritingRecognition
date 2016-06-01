from statistics import mode

import numpy as np

from utils.lists import flatten_one_level
from utils.functionArguments import kwargs_was_valid

default_parameters = {
    'white_threshold': 240
}


class SuspiciousSegmentationPointGenerator:
    """Class that generates the suspicious segmentation points

    Args:
        image (PIL.Image): A gray scale image in which we determine the suspicious segmentation points.
        white_threshold: The white threshold to be used, gray scales lower than this value are foreground, gray
            values greater than this value are background. Defaults to default_parameters['white_threshold'].
    """
    def __init__(self, image, **parameters):
        self._image = image
        self._stroke_width = _StrokeWidthComputer(image=image, **parameters).compute()


class SuspiciousSegmentationPoint:

     def __init__(self, x):
        self._x = x


class BaseLine:

    def __init__(self, high_y, low_y):
        self._high_y = high_y
        self._low_y = low_y

    @staticmethod
    def compute(image):
        pass


class _StrokeWidthComputer:
    """Class to compute the thickness of the pen stroke of a word in an image."""

    def __init__(self, image, **parameters):
        """The constructor of the StrokeWidthComputer class.

        Args:
            image (PIL.Image): A gray scale image in which we determine the stroke width.
            white_threshold: The white threshold to be used, gray scales lower than this value are foreground, gray
                values greater than this value are background.
        """
        self._image_array = np.array(image)
        self._white_threshold = parameters.pop(
            'white_threshold',
            default_parameters.get('white_threshold')
        )
        self._foreground = self._compute_foreground()
        kwargs_was_valid(kwargs=parameters, function_name='_StrokeWidthComputer Constructor')

    def compute(self):
        sequences = self._compute_continuous_foreground_sequences()
        return mode(sequences)

    def _compute_foreground(self):
        return self._image_array < self._white_threshold

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
