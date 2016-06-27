import sys

import numpy as np

from utils.things import Pixel, PixelPath
from utils.image import Image, ColorMode
from segmentation.binaryoversegmentation.segmentationlines import SegmentationLine


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
def distance_function(origin, destination,
                      is_fully_accessible, is_accessible_with_intersecting,
                      intersection_penalty=5, maximum_distance=sys.maxint):
    if is_fully_accessible:
        return origin.manhattan_distance_to(destination)
    if is_accessible_with_intersecting:
        return intersection_penalty * origin.manhattan_distance_to(destination)
    return maximum_distance


# def is_fully_accesible(destination, image):
#     return destination.is_background(image)
#
# def is_accessible_with_intersecting(destination, segmentation_line):
#     return destination.is_on(segmentation_line)


if __name__ == '__main__':
    image = Image(
        np.array([
            [1, 0, 1, 0, 0],
            [1, 1, 1, 0, 1],
            [1, 1, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ], dtype=np.uint8) * 255,
        color_mode=ColorMode.binary
    )

    segmentation_line = SegmentationLine(x=2)

    start = Pixel(row=3, column=2)
    end = Pixel(row=0, column=2)

    d_func = lambda origin, destination : distance_function(origin, destination,
                                                            is_fully_accessible=destination.is_background_in(image),
                                                            is_accessible_with_intersecting=destination.is_on(segmentation_line))

    # # Distance = 2
    # print(d_func(start, Pixel(row=2, column=2)))
    #
    # # Distance = 1
    # print(d_func(start, Pixel(row=3, column=3)))
    #
    # # Distance = max_int
    # print(d_func(end, Pixel(row=0, column=3)))

    path = PixelPath(AStar(image, start=start, goal=end, heuristic=heuristic, distance_function=d_func).path)
    print(path)
