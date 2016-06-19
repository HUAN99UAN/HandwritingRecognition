import interface


class BinaryOverSegmentation(interface.AbstractSegmenter):
    """Internal segmentation based on binary over segmentation.

    This method is based on Lee, Hong, and Brijesh Verma. "Binary segmentation algorithm for English cursive handwriting
    recognition." Pattern Recognition 45.4 (2012): 1306-1317.
    """

    def __init__(self, arg):
        super(BinaryOverSegmentation, self).__init__()

    def segment(self, image):
        raise NotImplementedError()

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
