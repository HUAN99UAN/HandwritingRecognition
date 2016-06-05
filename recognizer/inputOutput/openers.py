import os.path
import sys

from PIL import Image

import errors


class ImageOpener:

    def __init__(self, image_file_path):
        self.image_file_path = image_file_path

    def verify_image_file(self):
        if not (os.path.exists(self.image_file_path) and os.path.isfile(self.image_file_path)):
            raise errors.fileErrors.NonExistentFileError(
                "The file {} cannot be found.".format(
                    self.image_file_path)
            )

    def open(self):
        try:
            self.verify_image_file()
            image = Image.open(self.image_file_path)
        except:
            raise
        return image