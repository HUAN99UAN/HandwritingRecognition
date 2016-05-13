import annotationTree

class WordImage:

    def __init__(self, number, line_image, tree):
        self._line_image = line_image
        self._tree = tree
        self._number = number
        self._text = self._tree.get_text()
        self.image = self._extract_word_image()
        self._characters = self._build_character_dict()

    def _extract_word_image(self):
        # TODO nasty, fix this!
        page_image_copy = self._line_image._page_image.image.copy()
        bounding_box = self._tree.get_bounding_box()
        word_image = page_image_copy.crop(bounding_box)
        return word_image

    def _build_character_dict(selfself):
        characters = dict()
        print("_build_character_dict")
        return characters

    def __str__(self):
        return ", ".join([
            "{WordImage",
            "number: " + str(self._number),
            "text: " + self._text,
            "number of characters: " + str(len(self._characters)),
            "}"
        ])
