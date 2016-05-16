import tree
from annotationTree import AnnotationTree


class PageElementImage:
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
        self._tree = tree
        self._text = text
        self._image = image if image else self._extract_sub_image()

    @property
    def image(self):
        return self._image

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

    def _extract_sub_image(self):
        # The PIL documentation is vague about whether or not cropped images are cropped copies of the original
        # image, or new images. Just to be safe they are copied.
        source_image_copy = self.get_root().image.copy()
        bounding_box = self._tree.get_bounding_box()
        return source_image_copy.crop(bounding_box)

    def _repr_text(self):
        return self._text if self._text else "<None>"

    def _repr_image(self):
        return (", ".join([
            "{Image",
            "format: " + self._image.format,
            "}"
        ])) if self._image else str(None)

    def _repr_properties(self):
        return ",".join([
            "image: " + self._repr_image(),
            "tree: " + self._tree.__repr__(),
            "text: " + self._repr_text(),
        ])

    def __repr__(self):
        return "{PageElementImage - " + self._repr_properties() + "}"


class CharacterImage(tree.Leaf, PageElementImage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._text = self._tree.get_text()

    def __repr__(self):
        return "{CharacterImage - " + PageElementImage.__repr__(self) + " " + tree.Leaf.__repr__(self) + "}"


class WordImage(tree.Node, PageElementImage):

    annotation_tree_getter = AnnotationTree.characters
    child_element_constructor = CharacterImage

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_children(
            getter=WordImage.annotation_tree_getter,
            child_class_constructor=WordImage.child_element_constructor
        )

    def __repr__(self):
        return "{WordImage - " + PageElementImage.__repr__(self) + " " + tree.Node.__repr__(self) + "}"


class LineImage(tree.Node, PageElementImage):

    annotation_tree_getter = AnnotationTree.words
    child_element_constructor = WordImage

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_children(
            getter=LineImage.annotation_tree_getter,
            child_class_constructor=LineImage.child_element_constructor
        )

    def __repr__(self):
        return "{LineImage - " + PageElementImage.__repr__(self) + " " + tree.Node.__repr__(self) + "}"


class PageImage(tree.Root, PageElementImage):

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
        return "{PageImage - " + PageElementImage.__repr__(self) + " " + tree.Root.__repr__(self) + "}"
