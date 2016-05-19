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


class Stroke(shapes.Rectangle):
    """
    Representation of the strokes in the image used for the line segmentation.
    """

    def __init__(self, left_x_coordinate, right_x_coordinate, image):
        super(Stroke, self).__init__(
            top_left=Point(left_x_coordinate, 0),
            bottom_right=Point(right_x_coordinate, image.height)
        )
        self._image = image

    # @staticmethod
    # def stroke_coordinates(stroke_width, image_width):
    #     left = list(range(0, image_width, stroke_width))
    #     right = left[1:] + [image_width]
    #     return zip(left, right)

    # def _number_of_strokes(self, stroke_width):
    # import math
    #     image_width = self._image.size[1]
    #     return math.ceil(image_width / stroke_width)

    def paint(self, image=None):
        if not image:
            image = self._image
        self.paint_on(image)

    @staticmethod
    def compute_width():
        """
        The paper takes the mode of the width of the bottom reservoirs and multiplies that with the number of characters
        an average word has. The last is easily computed based on the training data. But the first is more difficult. For
        now we just say that strokes have some document independent width.
        """
        return 100

    @classmethod
    def strokes_in_image(cls, image, stroke_width):
        strokes = list()
        return strokes
