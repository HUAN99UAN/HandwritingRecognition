import annotationTree
import wordImage
import dataTree


class LineImage(dataTree.Node):
    """A image of a line with its meta information."""

    def __init__(self, number, page_image, tree):
        """
        Constructor fot a *LineImage*, a class representing a line of handwriting.

        Args:
            *number* The number, i.e. description of the image.
            *tree* The *AnnotationTree* with this page as its root.
        """
        self._tree = tree
        super(LineImage, self).__init__(
            image = self._extract_line_image(
                source_image=page_image.image
            ),
            description=number,
            parent=page_image
        )
        self.children = self._build_word_dict()

    @property
    def number(self):
        return self._description

    def _extract_line_image(self, source_image):
        # The PIL documentation is vague about whether or not cropped images are cropped copies of the original
        # image, or new images. Just to be safe they are copied.
        image_copy = source_image.copy()
        bounding_box = self._tree.get_bounding_box()
        line_image = image_copy.crop(bounding_box)
        return line_image

    def _build_word_dict(self):
        words = dict()
        for word in self._tree.words():
            child_tree = annotationTree.AnnotationTree(word)
            number = child_tree.get_number()
            words.update({
                number: wordImage.WordImage(
                    number=number,
                    line_image=self,
                    tree=child_tree
                )
            })
        return words

    def __repr__(self):
        return ", ".join([
            "{LineImage",
            "number: " + self._number,
            "number of words: " + str(len(self._words)),
            "}"
        ])