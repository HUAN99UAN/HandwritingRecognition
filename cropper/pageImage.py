import os

from PIL import Image

import annotationTree
import lineImage


class PageImage:

    def __init__(self, image_file, tree):
        self._tree = tree
        self._image_file = image_file
        self.image = ImageOpener(image_file).open()
        self._lines = self._build_line_dict()

    @property
    def image_file(self):
        return self._image_file

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

    def __str__(self):
        return ", ".join([
            "{PageImage",
            "number of lines: " + str(len(self._lines)),
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
