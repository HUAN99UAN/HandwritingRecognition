class TextBlockSegmenter:
    """
    Class that segments textblocks .
    """

    def __init__(self, image):
        self._image = image
        self._text_image = self._extract()

    def _extract(self):
        text_image = None
        return text_image