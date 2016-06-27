import sys

import numpy as np

from utils.things import Pixel
from utils.image import Image, ColorMode, InterpolationMethod


class AStar(object):
    """A Star in an image"""

    def __init__(self, image, start, goal, heuristic, distance_function, default_g_score=sys.maxint, default_f_score=sys.maxint):
        super(AStar, self).__init__()
        self._image = image
        self._start = start
        self._goal = goal

        self._closed_set = list()
        self._open_set = set()
        self._open_set.add(start)

        self._came_from = dict()

        self._heuristic = heuristic
        self._distance_function = distance_function

        self._g_score = {start: 0}
        self._f_score = {start: heuristic(start, goal)}

        self._default_g_score = default_g_score
        self._default_f_score = default_f_score

        self._path = list()

        self._search()

    def _search(self):
        while self._open_set and not self.has_path:
            current = self._get_current_node()
            self._review_node(current)

    def _get_current_node(self):
        current_pixel = min(self._open_set, key=lambda pixel: self._f_score.get(pixel, self._default_f_score))
        self._open_set.remove(current_pixel)
        self._closed_set.append(current_pixel)
        return current_pixel

    def _review_node(self, node):
        for neighbour in node.neighbours_in(self._image):
            if self.has_path:
                break
            self._review_neighbour(node, neighbour)

    def _review_neighbour(self, node, neighbour):
        if neighbour == self._goal:
            self.retrace_path(node)
            return

        if neighbour in self._closed_set:
            return

        self._open_set.add(neighbour)
        tentative_score = self._tentative_score(node=node, neighbour=neighbour)
        if tentative_score >= self._g_score.get(neighbour, self._default_g_score):
            return

        self._add_new_best_path(node, neighbour, score=tentative_score)

    def _add_new_best_path(self, node, neighbour, score):
        self._came_from[neighbour] = node
        self._g_score[neighbour] = score
        self._f_score[neighbour] = self._g_score.get(neighbour) + self._heuristic(neighbour, self._goal)

    def _tentative_score(self, node, neighbour):
        return self._g_score.get(node) + self._distance_function(node, neighbour)

    @property
    def path(self):
        return self._path

    @property
    def has_path(self):
        return bool(self._path)

    def retrace_path(self, current):
        path = [self._goal, current]
        while current in self._came_from.keys():
            current = self._came_from.get(current)
            path.append(current)
        self._path = list(reversed(path))

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


def heuristic(origin, destination):
    return origin.manhattan_distance_to(destination)

# This method should take the status of the pixel, foreground, background, on the segmentation_line, into account.
def distance_function(origin, destination):
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

    print(AStar(image, start=start, goal=end, heuristic=heuristic, distance_function=distance_function).path)
