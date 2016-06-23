import segmentation.binaryoversegmentation.baseline as baseline
import segmentation.binaryoversegmentation.strokewidth as strokewidth
import segmentation.interface
from postprocessing.lexicon import Lexicon
from segmentation.binaryoversegmentation.suspiciousregions import SuspiciousRegionsComputer
from segmentation.binaryoversegmentation.segmentationlines import SegmentationLines
import segmentation.binaryoversegmentation.segmentationlinesfilters as filters
from utils.image import Image
from utils.shapes import Rectangle
from utils.things import Point

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

        self._log = dict()

    def extract_body_bounding_box(self, image):
        return Rectangle(
            top_left=Point(x=0, y=self._high_base_line.y),
            bottom_right=Point(x=image.width, y=self._low_base_line.y)
        )

    def segment(self, image):
        self._low_base_line, self._high_base_line = self._base_line_estimator.estimate(image)
        self._stroke_width = self._stroke_width_estimator.estimate(image)

        body_region = image.sub_image(bounding_box=self.extract_body_bounding_box(image))

        suspicious_regions = SuspiciousRegionsComputer(threshold=self._stroke_width * 2).compute(body_region)
        self._log['suspicious_regions'] = suspicious_regions

        segmentation_lines = suspicious_regions.to_segmentation_lines(stroke_width=self._stroke_width)
        self._log['initial_segmentation_lines'] = segmentation_lines

        self._filter_segmentation_lines(image=image, segmentation_lines=segmentation_lines)

    def _filter_segmentation_lines(self, image, segmentation_lines):
        hole_filter = filters.HoleFilter(image=image)

        segmentation_lines = segmentation_lines.filter(hole_filter.keep)
        self._log['segmentation_lines_after_hole_filter'] = segmentation_lines

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


if __name__ == '__main__':
    from preprocessing.colorspaces import ToBinary

    image_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/word_2.png'
    image = Image.from_file(image_file)
    image = ToBinary().apply(image)

    lexicon_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/lexicon.txt'
    lexicon = Lexicon.from_file(lexicon_file)

    BinaryOverSegmentation(lexicon=lexicon).segment(image)
