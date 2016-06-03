class NoSuchAttributeError(Exception):
    def __init__(self, attribute, value):
        self.value = value
        self.attribute = attribute

    def __str__(self):
        return repr(self.value)

class InvalidElementPageElementError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidImageError(Exception):
    pass