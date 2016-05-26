class lazy_property(object):
    """"
    meant to be used for lazy evaluation of an object attribute.
    property should represent non-mutable data, as it replaces itself.

    source: http://stackoverflow.com/a/6849299/1357229
    """""

    def __init__(self, function):
        self.function = function
        self.function_name = function.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return None
        value = self.function(obj)
        setattr(obj, self.function_name, value)
        return value
