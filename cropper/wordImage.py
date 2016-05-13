import annotationTree

class WordImage:

    def __init__(self, number, line_image, tree):
        self._line_image = line_image
        self._tree = tree
        self.image = self._extract_word_image()
        self._number = number
        self._characters = self._build_character_dict()

    def _extract_word_image(self):
        word_image = None
        return word_image

    def _build_character_dict(selfself):
        characters = dict()
        print("_build_character_dict")
        return characters

    def __str__(self):
        return ", ".join([
            "{WordImage",
            "number: " + self._number,
            "number of characters: " + str(len(self._words)),
            "}"
        ])