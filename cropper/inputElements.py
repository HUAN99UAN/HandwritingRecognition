import dataTree
from annotationTree import AnnotationTree


class SomethingImage:
    """Representation of an element of a page of handwriting."""

    annotation_tree_getter = None
    child_element_constructor = None

    def __init__(self, image=None, tree=None, text=None, **kwargs):
        """
        Constructor of the somethingImage class
        :param image: image of the type *PIL.Image*
        :param tree: *AnnotationTree* representing the xml annotation of this element.
        :param text: Text represented by this element, is *None* if the text is unkown.
        :param kwargs:
        """
        super().__init__(**kwargs)
        self._image = image
        self._tree = tree
        self._text = None

    def _build_children(self, getter, child_class_constructor):
        self.children = dict()

        for element in getter(self._tree):
            child_tree = AnnotationTree(element)
            number = child_tree.get_number()
            self.children.update({
                number: child_class_constructor(
                    tree=child_tree,
                    description=number,
                    parent=self,
                    text=child_tree.get_text(default=None)
                )
            })

    def _repr_text(self):
        return self._text if self._text else "None"

    def _repr_image(self):
        return ", ".join([
            "{Image",
            "format: " + self._image.format,
            "}"
        ])

    def __repr__(self):
        return ", ".join([
            "{SomethingImage",
            "image: " + self._repr_image(),
            "tree: " + self._tree.__repr__(),
            "text: " + self._repr_text(),
            "}"
        ])


class CharacterImage(dataTree.Leaf, SomethingImage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._text = self._tree.get_text()

    def __repr__(self):
        return ", ".join([
            "{CharacterImage",
            "SomethingImage: " + SomethingImage.__repr__(self),
            "Leaf: " + dataTree.Leaf.__repr__(self),
            "}"
        ])


class WordImage(dataTree.Node, SomethingImage):

    annotation_tree_getter = AnnotationTree.characters
    child_element_constructor = CharacterImage

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_children(
            getter=WordImage.annotation_tree_getter,
            child_class_constructor=WordImage.child_element_constructor
        )

    def __repr__(self):
        return ", ".join([
            "{WordImage",
            "SomethingImage: " + SomethingImage.__repr__(self),
            "Node: " + dataTree.Node.__repr__(self),
            "}"
        ])


class LineImage(dataTree.Node, SomethingImage):

    annotation_tree_getter = AnnotationTree.words
    child_element_constructor = WordImage

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_children(
            getter=LineImage.annotation_tree_getter,
            child_class_constructor=LineImage.child_element_constructor
        )

    def __repr__(self):
        return ", ".join([
            "{LineImage",
            "SomethingImage: " + SomethingImage.__repr__(self),
            "Node: " + dataTree.Node.__repr__(self),
            "}"
        ])


class PageImage(dataTree.Root, SomethingImage):

    annotation_tree_getter = AnnotationTree.lines
    child_element_constructor = LineImage

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

    def __repr__(self):
        return ", ".join([
            "{PageImage",
            "SomethingImage: " + SomethingImage.__repr__(self),
            "Root: " + dataTree.Root.__repr__(self),
            "}"
        ])


