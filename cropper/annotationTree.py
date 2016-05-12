import os
import sys

import xml.etree.ElementTree as xmlTree


class AnnotationTree(xmlTree.ElementTree):

    def __init__(self, file_path):
        """A words file element hierarchy.

        This class represents the hierarchy of tagged elements in a words file.

        *file_path* is the file path of the words file, note that it should have the extension '.words'.

        """
        super(xmlTree.ElementTree, self).__init__()
        self._setroot(WordsFileOpener(file_path).open().getroot())

    @staticmethod
    def get_number(element):
        """Get the contents of the 'no' attribute of *element*

        *element* the element node of which we request the number

        Return the element number as a string.

        """
        print(element.get('bottom'))
        return element.get('no')

    @staticmethod
    def get_bounding_box(element):
        """Get the bounding box represented by *element*

        The bounding box is returned in the representation required by *PIL.Image.crop()*.

        *element* the element node of which we extract the bounding box.

        Return the bounding box as the tuple (left, rop, right, bottom).
        """
        return \
            int(element.get('left')), \
            int(element.get('top')), \
            int(element.get('right')), \
            int(element.get('bottom'))

    def get_image_file_name(self):
        """Get the image file name from the words file.

        Return the image file name, without extension.
        """
        return self.getroot().get('name')

    def lines(self):
        """Find all subelements with the tag 'TextLine'

        Return an iterable yielding all 'TextLine's in document order.

        """
        for line in self.iterfind('TextLine'):
            yield line

    def words(self):
        """Find all subelements with the tag 'Word'

        Return an iterable yielding all 'Words's in document order.

        """
        for word in self.iterfind('Word'):
            yield  word


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
                "Expected a file with the extension {}".format(
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