import segmentation.interface
from inputOutput import wordio as inputOutput
from recognizer import Recognizer
import postprocessing, segmentation
from utils.image import Image


class ValidationSegmentation(segmentation.interface.AbstractSegmenter):
    """
    Segmenter that uses the provided bounding boxes to segment the image, to validate the classifier and
    feature extractor.

    Note that this segmenter ONLY works if the recognizer is called with ONE image!!
    """

    def __init__(self, annotation):
        super(ValidationSegmentation, self).__init__()
        self._bounding_boxes = self._prepare_bounding_boxes(annotation)

    @classmethod
    def _prepare_bounding_boxes(cls, annotation):
        raise NotImplementedError()

    def segment(self, image):
        for bounding_box in self._bounding_boxes:
            yield image.sub_image(
                bounding_box=bounding_box,
                remove_white_borders=True,
            )


