import os
from collections import namedtuple

from xml.etree.ElementTree import ElementTree

from errors import InvalidElementPageElementError


BoundingBoxTuple = namedtuple('BoundingBox', ['left', 'top', 'right', 'bottom'])


class BoundingBox(BoundingBoxTuple):
    def __new__(cls, left, top, right, bottom):
        self = super(BoundingBox, cls).__new__(cls, left, top, right, bottom)
        try:
            self._validate()
        except:
            raise
        return self

    @staticmethod
    def _dimension_greater_than_zero(dimension):
        return dimension > 0

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top

    def _is_valid(self):
        try:
            return BoundingBox._dimension_greater_than_zero(self.width) and \
                   BoundingBox._dimension_greater_than_zero(self.height)
        except:
            raise

    def _validate(self):
        if not self._is_valid():
            raise InvalidElementPageElementError(
                "The {} has invalid dimensions.".format(self))


class AnnotationTree(ElementTree):
    """A words file element hierarchy.

    This class represents the hierarchy of tagged elements in a words file. To initialise it either an
    *element* or a *file_path* is required. Calling the constructor with *file_path* can cause the following
    exceptions:
        *NonExistentFileError* the file does not exist, or the path does not point to a file.
        *UnexpectedFileError* the does not have the extension of a words file.

    *element* is an optional root element node,
    *file* is an optional file handle or file name of an XML file whose
    contents will be used to initialize the _tree with.

    """
    def __init__(self, element=None, file_path=None):
        if file_path:
            WordsFileVerifier(file_path).verify()
        super(AnnotationTree, self).__init__(element, file_path)

    def get_number(self):
        """Get the contents of the 'no' attribute of the root.

        This method raises a NoSuchAttributeError if the root of the *AnnotationTree* does not have
        the attribute 'no'.

        Return the element number as an int.

        """
        number = self._get('no')
        return int(number)

    def _get(self, key):
        value = self.getroot().get(key)
        if not value:
            raise NoSuchAttributeError(
                key,
                "The element '{}' does not have the attribute '{}'.".format(
                    self.getroot().tag,
                    key
                )
            )
        return value

    def get_text(self, *args, **kwargs):
        """Get the contents of the 'text' attribute of the root.

        This method raises a NoSuchAttributeError if the root of the *AnnotationTree* does not have
        the attribute 'text', if no *default* is provided.

        Return the element text as a string.
        :param default: default return value if the element does not have the attribute 'text'. If no default value is
        passed a NoSuchAttributeError is raised instead.
        :return: the text attribute of the root of the annotation tree.
        """
        try:
            text = self._get('text')
        except NoSuchAttributeError as error:
            if args:
                text = args[0]
            elif 'default' in kwargs:
                text = kwargs.get('default')
            else:
                raise error
        return text

    def get_bounding_box(self):
        """Get the bounding box of the root of the _tree.

        The bounding box is returned in the representation required by *PIL.Image.crop()*.

        Return the bounding box as the tuple (left, rop, right, bottom).
        """
        try:
            bounding_box = BoundingBox(
                left=int(self._get('left')),
                top=int(self._get('top')),
                right=int(self._get('right')),
                bottom=int(self._get('bottom')))
            return bounding_box
        except NoSuchAttributeError as exception:
            raise NoSuchAttributeError(
                exception.attribute,
                'Could not build the bounding box of the element \'{}\', as it does not have the attribute \'{}\'.'.
                format(self.getroot().tag, exception.attribute)
            )
        except InvalidElementPageElementError:
            raise

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

    def __repr__(self):
        return ", ".join([
            "{ElementTree",
            "root tag: " + self._root.tag,
            "}"
        ])


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


class NonExistentFileError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NoSuchAttributeError(Exception):
    def __init__(self, attribute, value):
        self.value = value
        self.attribute = attribute

    def __str__(self):
        return repr(self.value)


class UnexpectedFileError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)