class Element:
    """
    Element of a tree.

    *image* is the image stored in the element, *description* is a description of the element.
    """
    def __init__(self, image = None, description = None):
        self._image = image
        self._description = description

    @property
    def description(self):
        return self._description

    @property
    def image(self):
        return self._image

    def __repr__(self):
        return ", ".join([
            "{Element",
            "description: " + self._description,
            "}"
        ])


class Root(Element):
    """
    Root of a tree.

    *content* is the actual content of the root, *description* is a description of the element. The dict *children*
    has as keys the description of the children and as values the children.
    """
    def __init__(self, image, description, children = None):
        super(Root, self).__init__(image, description)
        self._children = children

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    def __repr__(self):
        return ", ".join([
            "{Root",
            "description: " + self._description,
            "children: [" + " ".join(self._children.keys()) + "]",
            "}"
        ])


class Node(Root):
    """
    Root of a tree.

    *content* is the actual content of the root, *description* is a description of the element. The dict *children*
    has as keys the description of the children and as values the children. *parent* contains a reference to the parent
    of the node.
    """
    def __init__(self, image, description, parent, children=None):
        super(Node, self).__init__(image, description, children)
        self._parent = parent

    def __repr__(self):
        return ", ".join([
            "{Node",
            "description: " + self._description,
            "parent: " + self._parent.description,
            "children: [" + " ".join(self._children.keys()) + "]",
            "}"
        ])


class Leaf(Element):
    """
    Leaf of a tree.

    *content* is the actual content of the root, *description* is a description of the element. *parent* contains a
    reference to the parent
    of the node.
    """
    def __init__(self, image, description, parent):
        super(Leaf, self).__init__(image, description)
        self._parent = parent

    def __repr__(self):
        return ", ".join([
            "{Leaf",
            "description: " + self._description,
            "parent: " + self._parent.description,
            "}"
        ])