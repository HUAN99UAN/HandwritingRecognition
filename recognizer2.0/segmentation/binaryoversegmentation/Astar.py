import sys

import numpy as np

from utils.things import Pixel
from utils.image import Image, ColorMode, InterpolationMethod


class AStar(object):
    """A Star in an image"""

    def __init__(self, image, start, goal, heuristic, default_g_score=sys.maxint, default_f_score=sys.maxint):
        super(AStar, self).__init__()
        self._image = image
        self._start = start
        self._goal = goal

        self._closed_set = set(start)
        self._open_set = set()
        self._came_from = dict()

        self._heuristic = heuristic

        self._g_score = {start: 0}
        self._f_score = {start: heuristic(start, goal)}

        self._default_g_score = default_g_score
        self._default_f_score = default_f_score

        self._path = list()

        self._search()

    def _search(self):
        while self._open_set:
            current = self._get_current_node()
            self._review_node(current)

    def _get_current_node(self):
        min_idx = np.argmin(
            min(
                self._closed_set,
                key=lambda pixel : self._f_score.get(pixel, default=self._default_f_score)
            )
        )
        current = self._closed_set.pop(min_idx)
        self._open_set.add(current)
        return current

    def _review_node(self, node):
        for neighbour in node.neighbours_in(self._image):
            self._review_neighbour(node, neighbour)

    def _review_neighbour(self, node, neighbour):
        if neighbour is self._goal:
            self.retrace_path()

        tentative_score = self._g_score.get(node, self._default_g_score) + node.manhattan_distance_to(neighbour)
        self._open_set.add(neighbour)
        if tentative_score < self._g_score.get(neighbour, self._default_g_score):
            self._add_new_best_path(node, neighbour, score=tentative_score)

    def _add_new_best_path(self, node, neighbour, score):
        self._came_from[neighbour] = node
        self._g_score[neighbour] = score
        self._f_score[neighbour] = self._g_score.get(neighbour) + self._heuristic(neighbour, self._goal)

    @property
    def path(self):
        return self._path

    def retrace_path(self):
        self._path.append(self._goal)
        current = self._goal
        while current in self._came_from.keys():
            current = self._came_from.get(current)
            self._path.append(current)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


# This method should take the status of the pixel, foreground, background, on the segmentation_line, into account.
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

    AStar(image, start=start, goal=end, heuristic=heuristic)
