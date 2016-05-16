def delete_element_from_dict(key, dictionary):
    try:
        del dictionary[key]
    except KeyError:
        pass


class Node:
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
        super().__init__(**kwargs)

    def get_root(self):
        """
        Get the root of the tree this node is part of.

        :rtype: tree.Node
        :return: the root node of the tree.
        """
        return self.parent.get_root()

    def is_root(self):
        return False

    def _repr_description(self):
        return self._description if self._description else "None>"

    def _repr_children(self):
        return "[" + (" ".join(str(self.children.keys())) if self.children else "") + "]"

    def _repr_parent(self):
        return self.parent._description if self.parent else "None"

    def __repr__(self):
        return ", ".join([
            "{Node",
            "description: " + self._repr_description(),
            "parent: " + self._repr_parent(),
            "children: " + self._repr_children(),
            "}"
        ])


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

        super().__init__(
            description=description,
            parent=None,
            children=children,
            **kwargs)

    def get_root(self):
        return self

    def is_root(self):
        return True

    def __repr__(self):
        return ", ".join([
            "{Root",
            "description: " + self._repr_description(),
            "parent: " + self._repr_parent(),
            "children: " + self._repr_children(),
            "}"
        ])


class Leaf(Node):
    """
    Node of a tree.
    :param description: description of the node.
    :param parent: parent of this node, type should be *Node* or *Root*
    """
    def __init__(self, description=None, parent=None, **kwargs):
        delete_element_from_dict(dictionary=kwargs, key='children')
        super().__init__(
            description=description,
            parent=parent,
            children=None,
            **kwargs)

    def __repr__(self):
        return ", ".join([
            "{Leaf",
            "description: " + self._repr_description(),
            "parent: " + self._repr_parent(),
            "children: " + self._repr_children(),
            "}"
        ])