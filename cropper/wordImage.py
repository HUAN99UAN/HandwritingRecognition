import annotationTree
import characterImage
import tree


class WordImage(tree.Node):
    """A image of a word with its meta information."""

    def __init__(self, number, line_image, tree):
        self._tree = tree
        self._text = self._tree.get_text()

        super(WordImage, self).__init__(
            image=self._extract_word_image(
                # TODO nasty, fix this!
                source_image=line_image._parent.image),
            description=number,
            parent=line_image
        )
        self.children = self._build_character_dict()

    def _extract_word_image(self, source_image):
        source_image_copy = source_image.copy()
        bounding_box = self._tree.get_bounding_box()
        word_image = source_image_copy.crop(bounding_box)
        return word_image

    def _build_character_dict(self):
        characters = dict()
        for character in self._tree.characters():
            child_tree = annotationTree.AnnotationTree(character)
            number = child_tree.get_number()
            characters.update({
                number : characterImage.CharacterImage(
                    number=number,
                    word_image=self,
                    tree=annotationTree.AnnotationTree(element=character)
                )
            })
        return characters

    def __str__(self):
        return ", ".join([
            "{WordImage",
            "number: " + str(self._number),
            "text: " + self._text,
            "number of characters: " + str(len(self._characters)),
            "}"
        ])
