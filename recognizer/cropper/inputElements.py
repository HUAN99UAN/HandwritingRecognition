import sys
import os.path

from utils import tree
from annotationTree import AnnotationTree
from utils.decorators import lazy_property
from errors.inputErrors import InvalidElementPageElementError


def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=False)


class PageElementImage:
    """Representation of an element of a page of handwriting."""

    annotation_tree_getter = None
    child_element_constructor = None
    type_description = None

    def __init__(self, image=None, tree=None, text=None, **kwargs):
        """
        Constructor of the somethingImage class
        :param image: image of the type *PIL.Image*
        :param tree: *AnnotationTree* representing the xml annotation of this element.
        :param text: Text represented by this element, is *None* if the text is unkown.
        :param kwargs:
        """
        super().__init__(**kwargs)
        self._tree = tree
        self._text = text
        self._image = image

    def _build_child(self, element, constructor):
        child_tree = AnnotationTree(element)
        number = child_tree.number
        child = constructor(
            tree=child_tree,
            description=number,
            parent=self,
            text=child_tree.get_text(default=None)
        )
        return number, child

    def _build_children(self, getter, child_class_constructor):
        self.children = dict()
        for element in getter(self._tree):
            try:
                (number, child) = self._build_child(
                    constructor=child_class_constructor,
                    element=element)
                self.children.update({number: child})
            except InvalidElementPageElementError as error:
                # if the element is invalid we just skip it.
                print("Skipped one of the children of {} as {}".format(self.parent, error.value), file=sys.stderr)
                # pass

    def _extract_sub_image(self):
        # The PIL documentation is vague about whether or not cropped images are cropped copies of the original
        # image, or new images. Just to be safe they are copied.
        source_image = self.root.image
        return source_image.crop(self._bounding_box)

    def lines(self):
        return list()

    def words(self):
        return list()

    def characters(self):
        return list()

    def _repr_text(self):
        return self._text if self._text else "<None>"

    def _repr_image(self):
        return '{Image}' if self._image else '<none>'

    def _repr_properties(self):
        return ", ".join([
            "image: " + self._repr_image(),
            "tree: " + self._tree.__repr__(),
            "text: " + self._repr_text(),
        ])

    def __repr__(self):
        return "{PageElementImage - " + PageElementImage._repr_properties(self) + "}"

    def __str__(self):
        return "{}, {}({})".format(self.parent, self.type_description, self._description)

    def _output_image_name(self, extension):
        return '{type}_{description}.{extension}'.format(
            type=self.type_description,
            description=self._description,
            extension=extension
        )

    def _output_directory_name(self):
        return '{type}_{description}'.format(
            type=self.type_description,
            description=self._description
        )

    def _output_file_path(self, directory, extension):
        return os.path.join(directory, self._output_image_name(extension=extension))

    def image_to_file(self, directory, extension):
        image_file_path = self._output_file_path(directory=directory, extension=extension)
        try:
            self.image.save(image_file_path)
        except KeyError:
            print("Could not write the file {} as the output format could not be determined.".format(
                image_file_path), file=sys.stderr)
        except IOError:
            print("Could not write the file {} the created file may contain partial data.".format(
                image_file_path), file=sys.stderr)

    def images_to_file(self, directory, extension, element_getter):
        directory_path = os.path.join(directory, self._output_directory_name())
        create_directory(directory_path)
        self.image_to_file(directory=directory_path, extension=extension)
        for _, element in element_getter(self):
            element.images_to_file(directory=directory_path, extension=extension, element_getter=extension)


class CharacterImage(tree.Leaf, PageElementImage):

    type_description = 'character'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._text = self._tree.get_text(default=None)
        if not self._text:
            raise InvalidElementPageElementError('the text attribute of the element is undefined.')
        try:
            self._bounding_box = self._tree.get_bounding_box()
        except:
            raise

    @lazy_property
    def image(self):
        image = self._extract_sub_image()
        return image

    def images_to_file(self, directory, extension, element_getter):
        return self.image_to_file(directory=directory, extension=extension)

    def __repr__(self):
        return "{CharacterImage - " + PageElementImage.__repr__(self) + " " + tree.Leaf.__repr__(self) + "}"


class WordImage(tree.Node, PageElementImage):

    annotation_tree_getter = AnnotationTree.characters
    child_element_constructor = CharacterImage
    type_description = 'word'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_children(
            getter=WordImage.annotation_tree_getter,
            child_class_constructor=WordImage.child_element_constructor
        )
        try:
            self._bounding_box = self._tree.get_bounding_box()
        except:
            raise

    @lazy_property
    def image(self):
        image = self._extract_sub_image()
        return image

    def characters(self):
        return list(self.children.items())

    def images_to_file(self, directory, extension, element_getter):
        super(WordImage, self).images_to_file(directory=directory, extension=extension,
                                              element_getter=WordImage.characters)

    def __repr__(self):
        return "{WordImage - " + PageElementImage.__repr__(self) + " " + tree.Node.__repr__(self) + "}"


class LineImage(tree.Node, PageElementImage):

    annotation_tree_getter = AnnotationTree.words
    child_element_constructor = WordImage
    type_description = 'line'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_children(
            getter=LineImage.annotation_tree_getter,
            child_class_constructor=LineImage.child_element_constructor
        )
        try:
            self._bounding_box = self._tree.get_bounding_box()
        except:
            raise

    @lazy_property
    def image(self):
        image = self._extract_sub_image()
        return image

    def words(self):
        return list(self.children.items())

    def characters(self):
        characters = list()
        for _, word in self.words():
            characters = characters + word.characters()
        return characters

    def images_to_file(self, directory, extension, element_getter):
        super(LineImage, self).images_to_file(directory=directory, extension=extension, element_getter=LineImage.words)

    def __repr__(self):
        return "{LineImage - " + PageElementImage.__repr__(self) + " " + tree.Node.__repr__(self) + "}"


class PageImage(tree.Root, PageElementImage):

    annotation_tree_getter = AnnotationTree.lines
    child_element_constructor = LineImage
    type_description = 'page'

    def __init__(self, **kwargs):
        """
        PageImage constructor
        :param kwargs:
            :param image: image of the type *PIL.Image*
            :param tree: *AnnotationTree* representing the xml annotation of this element.
            :param description: description of the node.
            :param children: children of this node, type should be *Node* or *Leaf*
            :param kwargs:
        """
        super().__init__(**kwargs)
        self._build_children(
            getter=PageImage.annotation_tree_getter,
            child_class_constructor=PageImage.child_element_constructor)

    @property
    def image(self):
        return self._image

    def lines(self):
        return list(self.children.items())

    def words(self):
        words = list()
        for _, line in self.lines():
            words = words + line.words()
        return words

    def characters(self):
        characters = list()
        for _, line in self.lines():
            characters = characters + line.characters()
        return characters

    def images_to_file(self, directory, extension, element_getter=None):
        super(PageImage, self).images_to_file(directory=directory, extension=extension, element_getter=PageImage.lines)

    def __str__(self):
        return "{}({})".format(self.type_description, self._description)

    def __repr__(self):
        return "{PageImage - " + PageElementImage.__repr__(self) + " " + tree.Root.__repr__(self) + "}"
