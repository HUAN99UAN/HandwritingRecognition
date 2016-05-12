import wordsFile


class LineImage:

    def __init__(self, number, page_image, tree):
        self._page_image = page_image
        self._tree = tree
        self.image = self._extract_line_image()
        self._number = number
        self._words = self._build_word_dict()

    def __getattr__(self, item):
        if item == '_image':
            raise AttributeError()
        return getattr(self._image, item)

    def _extract_line_image(self):
        # The PIL documentation is vague about whether or not cropped images are cropped copies of the original
        # image, or new images. Just to be safe they are copied.
        page_image_copy = self._page_image.image.copy()
        bounding_box = wordsFile.WordsFile.get_bounding_box(self._tree)
        line_image = page_image_copy.crop(bounding_box)
        line_image.show()
        return line_image

    def _build_word_dict(self):
        words = dict()
        return words

    def __str__(self):
        return ", ".join([
            "{LineImage",
            "number: " + self._number,
            "number of words: " + str(len(self._words)),
            "}"])