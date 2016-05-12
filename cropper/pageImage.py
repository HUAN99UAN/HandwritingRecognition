import os

from PIL import Image

import annotationTree
import lineImage


class PageImage:

    def __init__(self, image_file, tree):
        self.tree = tree
        self.image = ImageOpener(image_file).open()
        self._lines = self._build_line_dict()

    def __getattr__(self, item):
        if item == 'image':
            raise AttributeError()
        return getattr(self._image, item)

    def _build_line_dict(self):
        lines = dict()

        for line in self.tree.lines():
            number = annotationTree.AnnotationTree.get_number(line)
            lines.update({
                number: lineImage.LineImage(
                    number=number,
                    page_image=self,
                    tree=line
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
