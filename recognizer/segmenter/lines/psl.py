import numpy as np

from utils import shapes


class JoinedPieceWiseSeparatingLines:
    def __init__(self):
        self._psls = list()

    def add_psl(self, psl):
        self._psls.append(psl)

    def paint(self, image):
        for psl in self._psls:
            psl.paint_on(image)
        return image

    @property
    def piece_wise_separating_lines(self):
        return self._psls

    @staticmethod
    def from_initial_psl(psl):
        line = JoinedPieceWiseSeparatingLines()
        current_psl = psl
        line.add_psl(current_psl)
        while current_psl.right_neighbour:
            current_psl = current_psl.right_neighbour
            line.add_psl(current_psl)
        return line


class PieceWiseSeparatingLine(shapes.HorizontalLine):
    def __init__(self, x1, x2, y):
        super(PieceWiseSeparatingLine, self).__init__(x1, x2, y)
        self._left_neighbour = None
        self._right_neighbour = None

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
    def is_joined_on_the_left(self):
        return self.left_neighbour is not None

    @property
    def is_joined_on_the_right(self):
        return self.right_neighbour is not None

    def join_to_psl_in_stripe(self, stripe, line_height, white_threshold):
        neighbour_psl = stripe.find_psl_at_height(height=self.y, tolerance=line_height / 2.0)
        if neighbour_psl:
            self.left_neighbour = neighbour_psl
            return
        else:
            new_psl = None
            # new_psl = self._extend_in_to_stripe(stripe, white_threshold=white_threshold)
            return new_psl

    def _extend_in_to_stripe(self, stripe, white_threshold):
        def is_white(line):
            return np.all(line > white_threshold)

        if is_white(stripe.line_at(self.y)):
            raise NotImplementedError('create psl that connects to current psl through this stripe')
        else:
            raise NotImplementedError('build psl pixel by pixel')