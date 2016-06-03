import os

import numpy as np

from errors.fileErrors import NonExistentFileError
from errors.fileErrors import UnexpectedFileError
from errors.inputErrors import InvalidImageError


class WordsFileVerifier:
    _words_file_extension = '.words'

    def __init__(self, file_path):
        self._file_path = file_path

    def _is_words_file(self):
        (_, extension) = os.path.splitext(self._file_path)
        return extension == WordsFileVerifier._words_file_extension

    def verify(self):
        if not self._is_words_file():
            raise UnexpectedFileError(
                "Expected a file with the extension {}".format(
                    WordsFileVerifier._words_file_extension)
            )
        if not (os.path.exists(self._file_path) and os.path.exists(self._file_path)):
            raise NonExistentFileError(
                "The file {} cannot be found.".format(
                    self._file_path)
            )


class WordImageVerifier:

    def __init__(self, image, white_threshold, **parameters):
        self._image = image
        self._image_array = np.array(image)
        self._white_threshold = white_threshold

    def _is_gray_scale(self):
        if not self._image.mode in ['1', 'L', 'I', 'F']:
            raise InvalidImageError("The word image is not gray scale.")
        else:
            return True

    def _has_foreground(self):
        foreground = self._image_array < self._white_threshold
        if not np.any(foreground):
            raise InvalidImageError('The word image does not have a foreground.')
        else:
            return True

    def validate(self):
        return self._is_gray_scale() and self._has_foreground()