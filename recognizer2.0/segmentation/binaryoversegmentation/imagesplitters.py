class _AbstractImageSplitter(object):

    def __init__(self):
        self._image = None
        self._segmentation_line = None

    def _clean_up(self):
        self._image = None
        self._segmentation_line = None

    def split(self, image, segmentation_line):
        self._image = image
        self._segmentation_line = segmentation_line
        self._split()
        self._clean_up()

    def _split(self):
        pass


class ForegroundPixelContourTracing(_AbstractImageSplitter):
    """Use foreground get_pixel contour tracing to split segment the image into two along the passed line."""

    def __init__(self, foreground_pixel_color=0):
        super(ForegroundPixelContourTracing, self).__init__()
        self._foreground_pixel_color = 0

    def _split(self):
        raise NotImplementedError()

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)