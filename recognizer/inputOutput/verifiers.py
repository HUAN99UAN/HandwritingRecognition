import os

from errors.fileErrors import NonExistentFileError
from errors.fileErrors import UnexpectedFileError


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