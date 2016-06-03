def delete_element_from_dict(key, dictionary):
    try:
        del dictionary[key]
    except KeyError:
        pass


class Node(object):
    """
    Node of a tree.
    """
    def __init__(self, description=None, parent=None, children=dict(), **kwargs):
        """
        Constructor of the Node class
        :param description: description of the node.
        :param parent: parent of this node, type should be *Node* or *Root*
        :param children: children of this node, type should be *Node* or *Leaf*
        :param kwargs:
        """
        self._description = description
        self.parent = parent
        self.children = children
        super(Node, self).__init__(**kwargs)

    @property
    def root(self):
        return self.parent.root

    def is_root(self):
        return False

    def _repr_description(self):
        return str(self._description) if self._description else "<None>"

    def _repr_children(self):
        return "[" + " ,".join([str(key) for key in self.children.keys()]) + "]"

    def _repr_parent(self):
        return str(self.parent._description) if self.parent else "None"

    def _repr_properties(self):
        return ", ".join([
            "description: " + self._repr_description(),
            "parent: " + self._repr_parent(),
            "children: " + self._repr_children(),
        ])

    def __repr__(self):
        return "{Node - " + self._repr_properties() + "}"


class Root(Node):
    """
    Root of a tree.
    """
    def __init__(self, description=None, children=dict(), **kwargs):
        """
        Constructor of the Root class
        :param description: description of the node.
        :param children: children of this node, type should be *Node* or *Leaf*
        :param kwargs:
        """
        delete_element_from_dict(key='parent', dictionary=kwargs)

        super(Root, self).__init__(
            description=description,
            parent=None,
            children=children,
            **kwargs)

    @property
    def root(self):
        return self

    def is_root(self):
        return True

    def __repr__(self):
        return "{Root - " + self._repr_properties() + "}"


class Leaf(Node):
    """
    Node of a tree.
    :param description: description of the node.
    :param parent: parent of this node, type should be *Node* or *Root*
    """
    def __init__(self, description=None, parent=None, **kwargs):
        delete_element_from_dict(dictionary=kwargs, key='children')
        super(Leaf, self).__init__(
            description=description,
            parent=parent,
            children=dict(),
            **kwargs)

    def __repr__(self):
        return "{Leaf - " + self._repr_properties() + "}"