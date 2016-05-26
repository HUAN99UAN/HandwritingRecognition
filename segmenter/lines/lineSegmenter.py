from collections import Counter

from lines.segmentedlines import SegmentedLines
from lines.stripe import Stripe

_default_parameters = {
    'white_threshold': 240,
    'number_of_most_frequent_values': 5,
    'line_height': 0
}

class LineSegmenter:
    """
    Class that segments lines based on the algorithm described in Tripathy, Nilamadhaba, and Umapada Pal. "Handwriting
    segmentation of unconstrained Oriya text." Sadhana 31.6 (2006): 755-769.
    """

    def __init__(self, image, **parameters):
        self._image = image
        self._stripes = Stripe.stripes_in_image(
            image=self._image,
            stripe_width=Stripe.compute_width()
        )
        self._parameters = _default_parameters.copy()
        self._parameters.update(parameters)
        self._lines = list()

    @property
    def parameters(self):
        return self._parameters

    @property
    def white_threshold(self):
        return self._parameters.get('white_threshold')

    @property
    def number_of_most_frequent_values(self):
        return self._parameters.get('number_of_most_frequent_values')

    @property
    def line_height(self):
        return self._parameters.get('line_height')

    @property
    def piece_wise_separating_lines(self):
        psls = list()
        [psls.extend(stripe.piece_wise_separating_lines) for stripe in self._stripes]
        return psls

    def segment(self):
        self._compute_piece_wise_separating_lines(self.white_threshold)
        self._remove_empty_margin_stripe()
        self._parameters['line_height'] = self._compute_line_height()
        self._filter_piece_wise_separating_lines()
        self._join_right_to_left()
        # self._join_left_to_right()
        # last filter
        self._lines = SegmentedLines.from_psls(self.piece_wise_separating_lines)

    def _compute_piece_wise_separating_lines(self, white_threshold):
        for stripe in self._stripes:
            stripe.compute_piece_wise_separating_lines(white_threshold)

    def _remove_empty_margin_stripe(self):
        self._remove_empty_left_margin_stripes()
        self._remove_empty_right_margin_stripes()

    def _remove_empty_left_margin_stripes(self):
        if not self._stripes[0].has_piece_wise_separating_lines():
            removed_stripe = self._stripes.pop(0)
            removed_stripe.right_neighbour.left_neighbour = None
            self._remove_empty_left_margin_stripes()

    def _remove_empty_right_margin_stripes(self):
        if not self._stripes[-1].has_piece_wise_separating_lines():
            removed_stripe = self._stripes.pop()
            removed_stripe.left_neighbour.right_neighbour = None
            self._remove_empty_right_margin_stripes()

    def _get_line_heights(self):
        line_heights = list()
        for stripe in self._stripes:
            line_heights.extend(stripe.distances_between_piece_wise_separating_lines())
        return line_heights

    def _compute_line_height(self):
        def get_minimum_of_most_frequent_values():
            counter = Counter(line_heights)
            return min(
                [height
                 for (height, _)
                 in counter.most_common(self.number_of_most_frequent_values)]
            )

        line_heights = self._get_line_heights()
        # according to the paper we should use the mode of the line heights, but the results were crappy.
        line_height = get_minimum_of_most_frequent_values()
        return line_height

    def _filter_piece_wise_separating_lines(self):
        for stripe in self._stripes:
            stripe.filter_piece_wise_separating_lines(self.line_height)

    def _join_left_to_right(self):
        raise NotImplementedError

    def _join_right_to_left(self):
        for stripe in reversed(self._stripes):
            stripe.join_piece_wise_separating_lines(line_height=self.line_height,
                                                    white_threshold=self.white_threshold)

    def _paint_stripe_property(self, stripe_paint_function, image):
        image = image or self._image
        for stripe in self._stripes:
            stripe_paint_function(stripe, image)
        return image

    def paint_stripes(self, image=None):
        return self._paint_stripe_property(stripe_paint_function=Stripe.paint, image=image)

    def paint_piece_wise_separating_lines(self, image=None):
        return self._paint_stripe_property(stripe_paint_function=Stripe.paint_piece_wise_separating_lines, image=image)

    def paint_lines(self, image=None):
        image = image or self._image
        self._lines.paint(image)
        return image


