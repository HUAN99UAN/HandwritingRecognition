class Image(object):
    """Class representing an image with an array like interface."""

    def __init__(self, arg):
        super(Image, self).__init__()
        self.arg = arg

    def sub_image(self, bounding_box):
        raise NotImplementedError()

    def show(self):
        raise NotImplementedError()

    @staticmethod
    def from_file(input_file):
        raise NotImplementedError()
