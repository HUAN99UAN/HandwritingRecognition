def kwargs_was_valid(kwargs, function_name):
    if kwargs:
        raise TypeError("The function '{function_name}' does not support the parameter(s) {parameters}.".format(
            function_name=function_name,
            parameters=", ".join("'{key}'".format(key = key) for key in kwargs.keys())
        ))