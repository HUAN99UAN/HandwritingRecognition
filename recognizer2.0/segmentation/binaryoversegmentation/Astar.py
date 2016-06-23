import numpy as np

from utils.things import Pixel
from utils.image import Image, ColorMode, InterpolationMethod


class AStar(object):
    """A Star in an image"""

    def __init__(self, image, start, goal, heuristic):
        super(AStar, self).__init__()
        self._image = image
        self._start = start
        self._goal = goal

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


def heuristic(origin, destination):
    return origin.manhattan_distance_to(destination)

if __name__ == '__main__':
    image = Image(
        np.array([
            [1, 0, 1, 0, 0],
            [1, 0, 1, 0, 1],
            [1, 1, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ], dtype=np.uint8) * 255,
        color_mode=ColorMode.binary
    )

    start = Pixel(row=3, column=2)
    end = Pixel(row=0, column=2)