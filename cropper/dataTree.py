class Node:
    """
    Node of a tree.
    """
    def __init__(self, description=None, parent=None, children=dict(), **kwargs):
        """
        Constructor of the Node class
        """
        print("Node")
        super().__init__(**kwargs)
        self._description = description
        self.parent = parent
        self.children = children

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
    def __init__(self, description=None, children=dict(), **kwargs):
        """
        Constructor of the Root class
        """
        print("Root")
        del kwargs['parent']
        super().__init__(
            description=description,
            parent=None,
            children=children,
            **kwargs)

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
    def __init__(self, description=None, parent=None, **kwargs):
        print("Leaf")
        del kwargs['children']
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