class Node:
    """
    Node of a tree.
    """
    def __init__(self, kwargs):
        """
        Constructor of the Node class
        :param kwargs: with the following keys:
            *description* description of the node
            *parent* parent of the node
            *children* dictionary with the description of the children as key, and the children as values.
        """
        super(Node, self).__init__()
        self._description = kwargs.get('description')
        self.parent = kwargs.get('parent')
        self.children = kwargs.get('children')

    def get_root(self):
        """
        Get the root of the tree this node is part of.

        :rtype: dataTree.Node
        :return: the root node of the tree.
        """
        return self.parent.get_root()

    def _repr_description(self):
        return self._description if self._description else "None>"

    def _repr_children(self):
        return "[" + (" ".join(self.children.keys()) if self.children else "") + "]"

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
    def __init__(self, **kwargs):
        """
        Constructor of the Root class
        :param kwargs: with the following keys:
            *description* description of the node
            *children* dictionary with the description of the children as key, and the children as values.
        """
        kwargs['parent'] = None
        super(Root, self).__init__(**kwargs)

    def get_root(self):
        return self

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
    """
    def __init__(self, **kwargs):
        """
        Constructor of the Root class
        :param kwargs: with the following keys:
            *description* description of the node
            *parent* parent of the node
        """
        kwargs['children'] = None
        super(Leaf, self).__init__(**kwargs)

    def __repr__(self):
        return ", ".join([
            "{Leaf",
            "description: " + self._repr_description(),
            "parent: " + self._repr_parent(),
            "children: " + self._repr_children(),
            "}"
        ])