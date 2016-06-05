from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET

import inputOutput.verifiers
from errors.inputErrors import NoSuchAttributeError, InvalidElementPageElementError
from utils.boundingBox import BoundingBox


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
    def __init__(self, element_tree=None, file_path=None):
        if file_path:
            inputOutput.verifiers.WordsFileVerifier(file_path).verify()
        super(AnnotationTree, self).__init__(element_tree, file_path)

    @property
    def number(self):
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
                "the element '{}' does not have the attribute '{}'.".format(
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
        except NoSuchAttributeError as error:
            raise InvalidElementPageElementError(error.value)
        except InvalidElementPageElementError:
            raise

    @property
    def image_file_name(self):
        """
        Get the image file name from the words file.
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

    def add_child(self, child):
        self.getroot().append(child)

    @staticmethod
    def from_input_element(input_element):
        return _AnnotationTreeBuilder(input_element).build()

    def to_file(self, output_file):
        _AnnotationTreeWriter(tree=self, output_file=output_file).write()

    def update_from_page_image(self, page_image):
        _AnnotationTreeUpdater(
            annotation_tree=self,
            page_image=page_image
        ).update()

    def __repr__(self):
        return ", ".join([
            "{ElementTree",
            "root tag: " + self._root.tag,
            "}"
        ])


class _AnnotationTreeBuilder(object):

    def __init__(self, input_element):
        self._element = input_element

    def build(self):
        element = ET.Element(
            tag=self._element.words_file_type,
            attrib=self._element.words_file_attributes
        )
        return AnnotationTree(element_tree=element)


class _AnnotationTreeWriter(object):

    def __init__(self, tree, output_file):
        self._tree = tree
        self._output_file = output_file

    def write(self):
        self._tree.write(self._output_file)


class _AnnotationTreeUpdater(object):

    def __init__(self, annotation_tree, page_image):
        self._tree = annotation_tree
        self._page_image = page_image

    def _update_word(self, tree, word):
        tree.getroot().set('text', word.text)

    def _update_words(self):
        for (_, word) in self._page_image.words():
            self._update_word(word.tree, word)

    def _update_character(self, tree, character):
        if character.tree:
            # update the character
            raise NotImplementedError()
        else:
            tree = _AnnotationTreeBuilder(character).build()
            character.tree = tree

    def _update_characters(self):
        for (_, character) in self._page_image.characters():
            self._update_character(character.tree, character)

    def _update_lines(self):
        # Lines never change, no need to update them right now
        pass

    def update(self):
        self._update_lines()
        self._update_words()
        self._update_characters()