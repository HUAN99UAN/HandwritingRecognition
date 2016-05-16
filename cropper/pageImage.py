import os

from PIL import Image

import annotationTree
import lineImage
import tree


class PageImage(tree.Root):
    """
    Representation of a image with handwiriting.
    """
    def __init__(self, image_file, tree):
        """
        Constructor for a *PageImage*.

        Args:
            *image_file* The complete path of the image file.
            *tree* The *AnnotationTree* with this page as its root.
        """
        self._tree = tree
        super(PageImage, self).__init__(
            image=ImageOpener(image_file).open(),
            description=image_file,
        )
        self.children = self._build_line_dict()

    @property
    def image(self):
        return self._image

    @property
    def image_file(self):
        return self._description

    def _build_line_dict(self):
        lines = dict()

        for line in self._tree.lines():
            child_tree = annotationTree.AnnotationTree(line)
            number = child_tree.get_number()
            lines.update({
                number: lineImage.LineImage(
                    number=number,
                    page_image=self,
                    tree=annotationTree.AnnotationTree(line)
                )
            })
        return lines

    def __repr__(self):
        return ", ".join([
            "{PageImage",
            "image file: " + self._description,
            "lines: {" + " ".join(self._children.keys()) + "]",
            "}"])


