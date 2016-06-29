import interface


class BackgroundBorderRemoval(interface.AbstractFilter):
    """Remove background borders"""

    def __init__(self, background_color=255):
        super(BackgroundBorderRemoval, self).__init__()
        self._background_color = 255

    def apply(self, image):
        super(BackgroundBorderRemoval, self).apply(image)
        raise NotImplementedError()

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)