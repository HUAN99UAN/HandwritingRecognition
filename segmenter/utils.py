from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


def mode(lst):
    """
    Returns the most frequent value of the list.
    :param lst: the iterable or mapping from which the most frequent value is to be computed.
    :return: the moest frequent value.
    """
    from collections import Counter
    counter = Counter(lst)
    return counter.most_common(1).pop(0)[0]
