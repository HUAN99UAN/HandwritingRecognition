import numpy as np

from utils.statistics import mode
from utils.image import WrongColorModeError
from utils.shapes import HorizontalLine
from preprocessing.invert import Invert


class _AbstractStrokeWidthEstimator(object):

    def __init__(self):
        super(_AbstractStrokeWidthEstimator, self).__init__()

    def estimate(self, image):
        pass


class RasterTechnique(_AbstractStrokeWidthEstimator):
    """
    This method has been proposed by Lee, Hong, and Brijesh Verma. "Binary segmentation algorithm for English cursive handwriting
    recognition." Pattern Recognition 45.4 (2012): 1306-1317.
    """

    def estimate(self, image):
        foreground = Invert().apply(image)
        sequence_lengths = self._find_continuous_sequences_lengths(foreground)
        return mode(sequence_lengths)

    @classmethod
    def _find_continuous_sequences_lengths(cls, image):
        sequences = list()
        sequences.extend(cls._find_continuous_sequences_lengths_along_horizontal_axis(image))
        sequences.extend(cls._find_continuous_sequences_lengths_along_horizontal_axis(np.transpose(image)))
        return sequences

    @classmethod
    def _find_continuous_sequences_lengths_along_horizontal_axis(cls, image):
        sequences = list()
        for sequence in image:
            sequences.extend(cls._find_continuous_sequences_lengths_in_row(sequence))
        return sequences

    @classmethod
    def _find_continuous_sequences_lengths_in_row(cls, bits):
        # source http://stackoverflow.com/a/1066838
        # make sure all runs of ones are well-bounded
        bounded = np.hstack(([0], bits, [0]))
        # get 1 at run starts and -1 at run ends
        difs = np.diff(bounded)
        run_starts, = np.where(difs > 0)
        run_ends, = np.where(difs < 0)
        return list(run_ends - run_starts)