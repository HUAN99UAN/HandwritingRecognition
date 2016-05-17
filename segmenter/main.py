import os
import sys

from PIL import Image


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
        image = None
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
    image_path_otsu_5 = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/segmenter/otsu_closing5.jpg'
    image_path_otsu_5_dilated_40 = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/segmenter/square.jpg'

    image_otsu_5 = ImageOpener(image_file_path=image_path_otsu_5).open()
    image_otsu_5_dilated_40 = ImageOpener(image_file_path=image_path_otsu_5_dilated_40).open()
    image_otsu_5_dilated_40.show()

    # pass image to textBlockSegmenter

