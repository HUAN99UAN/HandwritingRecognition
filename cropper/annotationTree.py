import os
import sys

from xml.etree.ElementTree import ElementTree


class AnnotationTree(ElementTree):
    """A words file element hierarchy.

    This class represents the hierarchy of tagged elements in a words file. To initialise it either an
    *element* or a *file_path* is required. If this is not the case a *MissingArgumentError* is raised. Calling
    the constructor with *file_path* can cause the following exceptions:
        *NonExistentFileError* the file does not exist, or the path does not point to a file.
        *UnexpectedFileError* the does not have the extension of a words file.

    *element* is an optional root element node,
    *file* is an optional file handle or file name of an XML file whose
    contents will be used to initialize the tree with.

    """
    def __init__(self, element=None, file_path=None):
        if not(element or file_path):
            raise MissingArgumentError("The AnnotationTree constructor requires either an element, or a filepath.")

        if file_path:
            WordsFileVerifier(file_path).verify()
        super(AnnotationTree, self).__init__(element, file_path)

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

        Return an iterable yielding all 'Word's in document order.

        """
        for word in self.iterfind('Word'):
            yield word

    def characters(self):
        """Find all subelements with the tag 'Character'

        Return an iterable yielding all 'Character's in document order.

        """
        for word in self.iterfind('Character'):
            yield word


class WordsFileVerifier:
    _words_file_extension = '.words'

    def __init__(self, file_path):
        self._file_path = file_path

    def _is_words_file(self):
        (_, extension) = os.path.splitext(self._file_path)
        return extension == WordsFileVerifier._words_file_extension

    def verify(self):
        if not (os.path.exists(self._file_path) and os.path.exists(self._file_path)):
            raise FileNotFoundError(
                "The file {} cannot be found.".format(
                    self._file_path)
            )
        if self._is_words_file():
            raise UnexpectedFileError(
                "Expected a file with the extension {}".format(
                    WordsFileVerifier._words_file_extension)
            )


class NonExistentFileError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class MissingArgumentError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UnexpectedFileError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)