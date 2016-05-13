import annotationTree


class CharacterImage:
    """A image of a character with its meta information."""

    def __init__(self, number, word_image, tree):
        self._word_image = word_image
        self._number = number
        self._tree = tree
        self._character = self._tree.get_text()
        self.image = self._extract_word_image()

    def _extract_word_image(self):
        page_image_copy = self._word_image._line_image._page_image.image.copy()
        bounding_box = self._tree.get_bounding_box()
        character_image = page_image_copy.crop(bounding_box)
        return character_image

    def __str__(self):
        return ", ".join([
            "{CharacterImage",
            "number: " + str(self._number),
            "character: " + self._character,
            "}"
        ])