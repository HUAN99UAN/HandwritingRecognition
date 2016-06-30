import numpy as np

import interface
import preprocessing.colorspaces
from utils.things import BoundingBox


class BackgroundBorderRemoval(interface.AbstractFilter):
    """Remove background borders"""

    def __init__(self):
        super(BackgroundBorderRemoval, self).__init__()

    def apply(self, image):
        super(BackgroundBorderRemoval, self).apply(image)
        bits = preprocessing.colorspaces.ToBinary(maximum_value=1).apply(image)
        try:
            top, bottom = self._compute_top_and_bottom(bits)
            left, right = self._compute_left_and_right(bits)
            return image.sub_image(
                BoundingBox(left=left, right=right, top=top, bottom=bottom),
                remove_white_borders=False
            )
        except ValueError:
            return image.EmptyImage(image.color_mode)

    def _compute_top_and_bottom(self, bits):
        row_bits = (np.sum(bits, axis=1) == bits.width)
        return self._get_initial_and_final_zeros_idx(row_bits)

    def _compute_left_and_right(self, bits):
        column_bits = (np.sum(bits, axis=0) == bits.height)
        return self._get_initial_and_final_zeros_idx(column_bits)

    def _get_initial_and_final_zeros_idx(self, bits):
        sequences = self._to_sequences(bits)
        left = 0
        right = len(bits) - 1

        if sequences:
            first_sequence = sequences.pop(0)
            if self.is_initial_border(first_sequence):
                left = first_sequence[1]
            if self.is_final_border(first_sequence, len(bits)):
                right = first_sequence[0] - 1

        if sequences:
            last_sequence = sequences.pop()
            if self.is_final_border(last_sequence, len(bits)):
                right = last_sequence[0] - 1
        return left, right

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