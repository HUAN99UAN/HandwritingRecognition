from utils.image import Image


class SegmentationImage(Image):
    """An image that is being segmented"""

    def __init__(self, arg):
        super(SegmentationImage, self).__init__()
        self.arg = arg

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
