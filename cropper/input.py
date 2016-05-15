import dataTree


class SomethingImage:
    """Representation of an element of a page of handwriting."""

    def __init__(self, image=None, tree=None, **kwargs):
        """
        Constructor of the somethingImage class
        """
        print("SomethingImage")
        super().__init__(**kwargs)
        self._image = image
        self._tree = tree


class PageImage(dataTree.Root, SomethingImage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("PageImage")


class LineImage:
    pass


class WordImage:
    pass


class CharacterImage:
    pass