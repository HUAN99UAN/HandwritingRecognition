import operator

import numpy as np

from utils import shapes
from segmenter.lines.psl import PieceWiseSeparatingLine
from utils.point import Point


class Stripe(shapes.Rectangle):
    """
    Representation of the stripes in the image used for the line segmentation.
    """

    def __init__(self, left_x, right_x, image, left_neighbour=None, right_neighbour=None):
        super(Stripe, self).__init__(
            top_left=Point(left_x, 0),
            bottom_right=Point(right_x, image.height)
        )
        self._image = image
        self._np_array = np.array(self._image).take(list(range(self.left, self.right)), 1)
        self._psl = None
        self._left_neighbour = left_neighbour
        self._right_neighbour = right_neighbour

    @property
    def left_neighbour(self):
        return self._left_neighbour

    @left_neighbour.setter
    def left_neighbour(self, value):
        self._left_neighbour = value
        if value and (not value.right_neighbour):
            value.right_neighbour = self

    @property
    def right_neighbour(self):
        return self._right_neighbour

    @right_neighbour.setter
    def right_neighbour(self, value):
        self._right_neighbour = value
        if value and (not value.left_neighbour):
            value.left_neighbour = self

    @property
    def piece_wise_separating_lines(self):
        return self._psl

    def line_at(self, height):
        return self._np_array.take([height], axis=0)

    def distances_between_piece_wise_separating_lines(self):
        return [
            pwl.distance_to(next_pwl)
            for (pwl, next_pwl)
            in zip(self._psl, self._psl[1:])
            ]

    def has_piece_wise_separating_lines(self):
        return len(self._psl) > 0

    def compute_piece_wise_separating_lines(self, white_threshold):
        """
        Compute the piece wise separating lines, consider any gray scale value greater than white as white.

        The computed piece wise separating lines are stored in self._psl.

        :param white_threshold: any element with a grayscale value greater than white is considered white.

        """

        def get_first_of_consecutive_values(array):
            # [1, 2, 3, 5, 6, 8] -> [1, 5, 8]"
            if len(array) is 1:
                return array
            else:
                return [current
                        for (previous, current)
                        in zip(array, array[1:])
                        if current - previous != 1]

        white_line_idx = self._find_white_lines(white_threshold=white_threshold)
        psl_idx = get_first_of_consecutive_values(white_line_idx)
        self._psl = [PieceWiseSeparatingLine(x1=self.left, x2=self.right, y=y) for y in psl_idx]

    def _find_white_lines(self, white_threshold):
        """
        Find the lines in this stripe where there are only white pixels.

        Return indices of lines where all pixels values are greater than the white threshold.
        """
        array = self._np_array
        white_line_logical = np.apply_along_axis(
            all,
            1,
            array > white_threshold
        )
        return np.array(range(0, len(white_line_logical)))[white_line_logical]

    def filter_piece_wise_separating_lines(self, line_height):
        """
        Remove a psl' if the distance between it and its neighbour is smaller than line_height_mode
        """

        def distance_within_range(distance):
            return distance >= line_height

        filtered_pbl = [self._psl[0]]
        for (previous_idx, current_idx) in zip(range(0, len(self._psl)), range(1, len(self._psl))):
            previous = self._psl[previous_idx]
            current = self._psl[current_idx]
            if distance_within_range(previous.distance_to(current)):
                filtered_pbl.append(current)
        self._psl = filtered_pbl

    def join_piece_wise_separating_lines(self, line_height, white_threshold):
        new_psls = list()
        for psl in self._psl:
            if not psl.is_joined_on_the_left and self.left_neighbour:
                new_psl = psl.join_to_psl_in_stripe(self.left_neighbour,
                                                    line_height=line_height,
                                                    white_threshold=white_threshold)
                if new_psls:
                    new_psl.append(new_psl)
        self._psl.extend(new_psls)

    def find_psl_at_height(self, height, tolerance):
        distances = [(psl, abs(psl.y - height)) for psl in self._psl]
        closest_psl = min(distances, key=operator.itemgetter(1))
        return_value = closest_psl[0] if closest_psl[1] < tolerance else None
        return return_value

    def paint(self, image=None):
        image = image or self._image
        self.paint_on(image)
        return image

    def paint_piece_wise_separating_lines(self, image=None):
        image = image or self._image
        for line in self._psl:
            line.paint_on(image)
        return image

    @staticmethod
    def compute_width():
        """
        The paper takes the mode of the width of the bottom reservoirs and multiplies that with the number of characters
        an average word has. The last is easily computed based on the training data. But the first is more difficult. For
        now we just say that stripes have some document independent width.
        """
        return 120

    @classmethod
    def stripes_in_image(cls, image, stripe_width):
        def compute_coordinates():
            left = list(range(0, image.width, stripe_width))
            right = left[1:] + [image.width]
            return list(zip(left, right))

        def set_neighbours():
            neighbour_pairs = zip(stripes, stripes[1:])
            for (stripe, right_neighbour) in neighbour_pairs:
                stripe.right_neighbour = right_neighbour

        coordinates = compute_coordinates()
        stripes = [
            Stripe(left_x=left, right_x=right, image=image)
            for (left, right) in coordinates]

        set_neighbours()
        return stripes