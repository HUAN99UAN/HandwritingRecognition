from tree import Leaf


class CharacterImage(Leaf):
    """A image of a character with its meta information."""

    def __init__(self, number, word_image, tree):
        self._tree = tree
        self._text = self._tree.get_text()

        super(CharacterImage, self).__init__(
            image = self._extract_character_image(
                # TODO nasty, fix this!
                source_image = word_image._parent._parent.image),
            description=number,
            parent=word_image
        )

    def _extract_character_image(self, source_image):
        page_image_copy = source_image.copy()
        bounding_box = self._tree.get_bounding_box()
        character_image = page_image_copy.crop(bounding_box)
        return character_image

    def __repr__(self):
        return ", ".join([
            "{CharacterImage",
            "number: " + str(self._number),
            "character: " + self._text,
            "}"
        ])
