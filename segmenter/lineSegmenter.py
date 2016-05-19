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

    def paint_strokes(self, image = None):
        if not image:
            image = self._image
        for stroke in self._strokes:
            stroke.paint(image)
        return image


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

    def paint(self, image=None):
        if not image:
            image = self._image
        self.paint_on(image)
        return image

    @staticmethod
    def compute_width():
        """
        The paper takes the mode of the width of the bottom reservoirs and multiplies that with the number of characters
        an average word has. The last is easily computed based on the training data. But the first is more difficult. For
        now we just say that strokes have some document independent width.
        """
        return 250

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
