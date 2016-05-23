import os
import sys

from PIL import Image, ImageDraw

import lineSegmenter
from utils import Point


class NonExistentFileError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ImageOpener:

    def __init__(self, image_file_path):
        self.image_file_path = image_file_path

    def verify_image_file(self):
        if not (os.path.exists(self.image_file_path) and os.path.isfile(self.image_file_path)):
            raise NonExistentFileError(
                "The file {} cannot be found.".format(
                    self.image_file_path)
            )

    def open(self):
        try:
            self.verify_image_file()
            image = Image.open(self.image_file_path)
        except IOError:
            sys.stderr.write("Could not read the file {}".format(self.image_file_path))
            sys.exit(-1)
        except NonExistentFileError as error:
            sys.stderr.write(str(error))
            sys.exit(-1)
        return image

if __name__ == '__main__':
    image_path = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/segmenter/final.jpg'
    image = ImageOpener(image_file_path=image_path).open()
    l = lineSegmenter.LineSegmenter(image=image)
    l.segment()

    image = l.paint_strokes()
    image = l.paint_piece_wise_separating_lines(image)
    image.show()
