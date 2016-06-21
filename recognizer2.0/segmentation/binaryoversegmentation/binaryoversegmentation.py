import segmentation.interface
import segmentation.binaryoversegmentation.baseline as baseline
from utils.image import Image
from postprocessing.lexicon import Lexicon

red = (0, 0, 255)
blue = (255, 0, 0)

class BinaryOverSegmentation(segmentation.interface.AbstractSegmenter):
    """Internal segmentation based on binary over segmentation.

    This method is based on Lee, Hong, and Brijesh Verma. "Binary segmentation algorithm for English cursive handwriting
    recognition." Pattern Recognition 45.4 (2012): 1306-1317.
    """

    def __init__(self, lexicon, max_segmentation=12, stroke_width_estimator=baseline.VerticalHistogram()):
        super(BinaryOverSegmentation, self).__init__()
        self._max_segmentation = max_segmentation
        self._base_line_estimator = stroke_width_estimator
        self._lexicon = lexicon

        # Depend on the input image, but are handy to store in the object.
        self._low_base_line = None
        self._high_base_line = None

    def segment(self, image):
        self._low_base_line, self._high_base_line = self._base_line_estimator.estimate(image)
        image = self._low_base_line.paint_on(image, color=red)
        image = self._high_base_line.paint_on(image, color=blue)
        image.show(wait_key=0)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


if __name__ == '__main__':
    from preprocessing.colorspaces import ToBinary

    image_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/word.png'
    image = Image.from_file(image_file)
    image = ToBinary().apply(image)

    BinaryOverSegmentation().segment(image)
