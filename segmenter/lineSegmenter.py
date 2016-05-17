import math


class LineSegmenter:
    """
    Class that segments lines based on the algorithm described in Tripathy, Nilamadhaba, and Umapada Pal. "Handwriting
    segmentation of unconstrained Oriya text." Sadhana 31.6 (2006): 755-769.
    """

    def __init__(self, image):
        self._image = image
        self._strokes = self._compute_strokes()

    def _compute_strokes(self):
        strokes = list()
        stroke_width = Stroke.compute_width()
        # image_width = self._image.size[1]
        image_width = 10
        for stroke_width in Stroke.stroke_widths(stroke_width, image_width):
            print(stroke_width)
        return strokes

    def _number_of_strokes(self, stroke_width):
        image_width = self._image.size[1]
        return math.ceil(image_width / stroke_width)


class Stroke:
    """
    Representation of the strokes in the image used for the line segmentation.
    """

    def __init__(self, width):
        self._width = width

    @staticmethod
    def stroke_widths(stroke_width, image_width):
        number_of_normal_strokes = math.floor(image_width / stroke_width)
        odd_stroke_size = image_width % stroke_width
        odd_stroke = [odd_stroke_size] if odd_stroke_size is not 0 else list()
        return ([stroke_width] * number_of_normal_strokes) + odd_stroke

    @staticmethod
    def compute_width():
        return 3
