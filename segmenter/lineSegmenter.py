import numpy as np

from utils import Point
import shapes


class LineSegmenter:
    """
    Class that segments lines based on the algorithm described in Tripathy, Nilamadhaba, and Umapada Pal. "Handwriting
    segmentation of unconstrained Oriya text." Sadhana 31.6 (2006): 755-769.
    """

    def __init__(self, image):
        self._image = image
        self._strokes = Stroke.strokes_in_image(
            image=self._image,
            stroke_width=Stroke.compute_width()
        )

    def compute_piece_wise_separating_lines(self):
        for stroke in self._strokes:
            stroke.compute_piece_wise_separating_lines()

    def _paint_stroke_property(self, stroke_paint_function, image):
        image = image or self._image
        for stroke in self._strokes:
            stroke_paint_function(stroke, image)
        return image

    def paint_strokes(self, image = None):
        return self._paint_stroke_property(stroke_paint_function=Stroke.paint, image=image)

    def paint_piece_wise_separating_lines(self, image = None):
        return self._paint_stroke_property(stroke_paint_function=Stroke.paint_piece_wise_separating_lines, image=image)


class Stroke(shapes.Rectangle):
    """
    Representation of the strokes in the image used for the line segmentation.
    """

    def __init__(self, left_x, right_x, image):
        super(Stroke, self).__init__(
            top_left=Point(left_x, 0),
            bottom_right=Point(right_x, image.height)
        )
        self._image = image
        self._pwl = list()

    @property
    def as_numpy_array(self):
        array = np.array(self._image)
        return array.take(list(range(self.left, self.right)), 1)

    def compute_piece_wise_separating_lines(self, white_threshold = 240):
        """
        Compute the piece wise separating lines, consider any gray scale value greater than white as white.

        The computed piece wise separating lines are stored in self._pwl.

        :param white_threshold: any element with a grayscale value greater than white is considered white.

        """
        def get_first_of_consecutive_values(array):
            if len(array) is 1:
                return array
            else:
                return [current
                    for (previous, current)
                    in zip(array, array[1:])
                    if current - previous != 1]

        white_line_idx = self._find_white_lines(white_threshold=white_threshold)
        pbl_idx = get_first_of_consecutive_values(white_line_idx)
        self._pwl = [shapes.Line.horizontal_line(x1=self.left, x2=self.right, y=y) for y in pbl_idx]

    def _find_white_lines(self, white_threshold):
        """
        Find the lines in this stroke where there are only white pixels.

        Return indices of lines where all pixels values are greater than the white threshold.
        """
        array = self.as_numpy_array
        white_line_logical = np.apply_along_axis(
            all,
            1,
            array > white_threshold
        )
        return np.array(range(0, len(white_line_logical)))[white_line_logical]

    def paint(self, image=None):
        image = image or self._image
        self.paint_on(image)
        return image

    def paint_piece_wise_separating_lines(self, image=None):
        image = image or self._image
        for line in self._pwl:
            line.paint_on(image)
        return image

    @staticmethod
    def compute_width():
        """
        The paper takes the mode of the width of the bottom reservoirs and multiplies that with the number of characters
        an average word has. The last is easily computed based on the training data. But the first is more difficult. For
        now we just say that strokes have some document independent width.
        """
        return 50

    @classmethod
    def strokes_in_image(cls, image, stroke_width):
        def compute_coordinates():
            left = list(range(0, image.width, stroke_width))
            right = left[1:] + [image.width]
            return list(zip(left, right))

        coordinates = compute_coordinates()
        strokes = [
            Stroke(left_x=left, right_x=right, image=image)
            for (left, right) in coordinates]
        return strokes
