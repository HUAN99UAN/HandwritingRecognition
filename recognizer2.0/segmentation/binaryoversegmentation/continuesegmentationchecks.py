class _AbstractContinueSegmentationCheck(object):

    def __init__(self):
        super(_AbstractContinueSegmentationCheck, self).__init__()

    def continue_segmentation(self, image):
        pass

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class ContinueOnWidthCheck(_AbstractContinueSegmentationCheck):
    """
    Segment the image further if its width is greater than minimum_character_width + average_character_width.
    """
    def __init__(self, minimum_character_width, average_character_width):
        super(ContinueOnWidthCheck, self).__init__()
        self._maximum_image_width = minimum_character_width + average_character_width

    def continue_segmentation(self, image):
        return image.width > self._maximum_image_width


class ContinueOnSSPCheck(_AbstractContinueSegmentationCheck):
    """
    Segment the image further if it has SSP left.
    """
    def __init__(self):
        super(ContinueOnSSPCheck, self).__init__()

    def continue_segmentation(self, image):
        return image.has_segmentation_lines
