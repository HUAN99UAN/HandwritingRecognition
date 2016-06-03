import itertools


def flatten_one_level(lst):
    return list(itertools.chain(*lst))