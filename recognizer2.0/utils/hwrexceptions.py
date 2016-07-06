class InvalidImageException(Exception):
    def __init__(self, image_file, *args, **kwargs):
        super(InvalidImageException, self).__init__("The image file {} is invalid".format(image_file), *args, **kwargs)
