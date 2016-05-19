from collections import namedtuple
from typing import TypeVar

IntFloat = TypeVar('IntFloat', int, float)

Point = namedtuple('Point', ['x', 'y'])