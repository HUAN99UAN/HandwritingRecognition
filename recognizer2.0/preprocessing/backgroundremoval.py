import interface
from preprocessing.colorspaces import ToBinary

import numpy as np


class BackgroundBorderRemoval(interface.AbstractFilter):
    """Remove background borders"""

    def __init__(self):
        super(BackgroundBorderRemoval, self).__init__()

    def apply(self, image):
        super(BackgroundBorderRemoval, self).apply(image)
        bits = ToBinary(maximum_value=1).apply(image)
        bits = self._remove_white_rows(bits)
        bits = self._remove_white_columns(bits)
        return bits * 255

    def _remove_white_rows(self, bits):
        row_bits = (np.sum(bits, axis=1) == bits.width)
        non_border_rows_idx = self._get_initial_and_final_zeros_idx(row_bits)
        return bits[non_border_rows_idx, ]

    def _remove_white_columns(self, bits):
        column_bits = (np.sum(bits, axis=0) == bits.height)
        non_border_columns_idx = self._get_initial_and_final_zeros_idx(column_bits)
        return bits[:,non_border_columns_idx]

    def _get_initial_and_final_zeros_idx(self, bits):
        sequences = self._to_sequences(bits)
        left = 0
        right = len(bits)

        if sequences:
            first_sequence = sequences.pop(0)
            if self.is_initial_border(first_sequence):
                left = first_sequence[1]
            if self.is_final_border(first_sequence, len(bits)):
                right = first_sequence[0]

        if sequences:
            last_sequence = sequences.pop()
            if self.is_final_border(last_sequence, len(bits)):
                right = last_sequence[0]
        return range(left, right)

    @classmethod
    def is_initial_border(cls, sequence):
        return sequence[0] == 0

    @classmethod
    def is_final_border(cls, sequence, length):
        return sequence[1] == length

    @classmethod
    def _to_sequences(cls, bits):
        bounded = np.hstack(([0], bits, [0]))
        difs = np.diff(bounded)
        run_starts, = np.where(difs > 0)
        run_ends, = np.where(difs < 0)
        return zip(run_starts, run_ends)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)