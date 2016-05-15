import os

from PIL import Image

import annotationTree
import lineImage
import dataTree


class PageImage(dataTree.Root):
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


class ImageOpener:

    def __init__(self, image_file_path):
        self.image_file_path = image_file_path

    def _file_can_be_opened(self):
        return \
            os.path.exists(self.image_file_path) and \
            os.path.isfile(self.image_file_path)

    def open(self):
        image = None
        if self._file_can_be_opened():
            try:
                image = Image.open(self.image_file_path)
            except IOError:
                import sys
                sys.stderr.write("Could not read the file {}".format(self.image_file_path))
        return image
