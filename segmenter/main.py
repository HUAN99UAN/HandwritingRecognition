import os

from PIL import Image


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

if __name__ == '__main__':
    image_path = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/otsu_closing5.jpg'
    image = ImageOpener(image_file_path=image_path).open()
    image.show()
    # pass image to lineSegmenter

