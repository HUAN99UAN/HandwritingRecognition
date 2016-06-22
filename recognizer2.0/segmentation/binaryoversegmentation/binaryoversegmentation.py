import segmentation.binaryoversegmentation.baseline as baseline
import segmentation.binaryoversegmentation.strokewidth as strokewidth
import segmentation.interface
from postprocessing.lexicon import Lexicon
from segmentation.binaryoversegmentation.suspiciousregions import SuspiciousRegionsComputer
from utils.image import Image

red = (0, 0, 255)
blue = (255, 0, 0)


class BinaryOverSegmentation(segmentation.interface.AbstractSegmenter):
    """Internal segmentation based on binary over segmentation.

    This method is based on Lee, Hong, and Brijesh Verma. "Binary segmentation algorithm for English cursive handwriting
    recognition." Pattern Recognition 45.4 (2012): 1306-1317.
    """

    def __init__(self, lexicon,
                 base_line_estimator=baseline.VerticalHistogram(),
                 stroke_width_estimator=strokewidth.RasterTechnique()):

        super(BinaryOverSegmentation, self).__init__()
        self._lexicon = lexicon
        self._max_segmentation = lexicon.longest_word.length
        self._base_line_estimator = base_line_estimator
        self._stroke_width_estimator = stroke_width_estimator

        # Depend on the input image, but are handy to store in the object.
        self._low_base_line = None
        self._high_base_line = None
        self._stroke_width = None

    def segment(self, image):
        self._low_base_line, self._high_base_line = self._base_line_estimator.estimate(image)
        self._stroke_width = self._stroke_width_estimator.estimate(image)
        suspicious_regions = SuspiciousRegionsComputer(threshold=self._stroke_width * 2).compute(image)
        segmentation_lines = suspicious_regions.to_segmentation_lines()

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


if __name__ == '__main__':
    from preprocessing.colorspaces import ToBinary

    image_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/word.png'
    image = Image.from_file(image_file)
    image = ToBinary().apply(image)

    lexicon_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/lexicon.txt'
    lexicon = Lexicon.from_file(lexicon_file)

    BinaryOverSegmentation(lexicon=lexicon).segment(image)
