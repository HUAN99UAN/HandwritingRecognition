import os

from PIL import Image


class PageImage:

    def __init__(self, image_file, words_file):
        self._words_file = words_file
        self._image = ImageOpener(image_file).open()
        self._lines = dict()

    def __getattr__(self, item):
        if item == '_image':
            raise AttributeError()
        return getattr(self._image, item)


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
