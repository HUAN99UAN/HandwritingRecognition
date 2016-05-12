import os
import sys

import xml.etree.ElementTree as xmlTree


class WordsFile:

    def __init__(self, file_path):
        self._file_path = file_path
        self._tree = WordsFileOpener(self._file_path).open()

    @staticmethod
    def get_bounding_box(element):
        return \
            int(element.get('left')), \
            int(element.get('top')), \
            int(element.get('right')), \
            int(element.get('bottom'))

    def get_image_file_name(self):
        return self._tree.getroot().get('name')

    def line_generator(self):
        for line in self._tree.getroot().iter('TextLine'):
            yield line


class WordsFileOpener:
    _words_file_extension = '.words'

    def __init__(self, file_path):
        self._file_path = file_path

    def open(self):
        tree = None
        error_message = None
        try:
            self._file_can_be_opened()
            tree = xmlTree.parse(self._file_path)
        except xmlTree.ParseError:
            error_message = "Parse error while parsing the file {}.".format(self._file_path)
        except FileExistsError:
            error_message = "The file {} does not exists.".format(self._file_path)
        except FileNotFoundError:
            error_message = "The file {} cannot be found.".format(self._file_path)
        except UnexpectedFileError:
            error_message = "Expected a file with the extension \'{}\'.".format(WordsFileOpener._words_file_extension)
        finally:
            if error_message:
                sys.stderr.write(error_message)
        return tree

    def _file_can_be_opened(self):
        if not os.path.exists(self._file_path):
            raise FileExistsError
        if not os.path.isfile(self._file_path):
            raise FileNotFoundError
        if not self._is_words_file():
            raise UnexpectedFileError(
                "Expected af file with the extension {}".format(
                    WordsFileOpener._words_file_extension)
            )

    def _is_words_file(self):
        (_, extension) = os.path.splitext(self._file_path)
        return extension == WordsFileOpener._words_file_extension


class UnexpectedFileError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)