import sys

import numpy as np

from segmentation.binaryoversegmentation.astar import AStar
from utils.things import Pixel, PixelPath
from utils.image import Image, ColorMode
from segmentation.binaryoversegmentation.segmentationlines import SegmentationLine
from preprocessing.colorspaces import ToBinary


def default_distance_function(origin, destination,
                              is_fully_accessible, is_accessible_with_intersecting,
                              intersection_penalty=5, maximum_distance=sys.maxint):
    if is_fully_accessible:
        # return origin.manhattan_distance_to(destination)
        return 1
    if is_accessible_with_intersecting:
        # return intersection_penalty * origin.manhattan_distance_to(destination)
        return intersection_penalty
    return maximum_distance


def default_heuristic(origin, destination):
    return origin.manhattan_distance_to(destination)


def default_neighbour_filter(node, segmentation_line, character_width):
    left_boundary = segmentation_line.x - character_width
    right_boundary = segmentation_line.x + character_width + 1
    return node.x in range(left_boundary, right_boundary)


class _AbstractImageSplitter(object):

    def __init__(self):
        self._image = None
        self._segmentation_line = None
        self._pixel_path = None

    def _clean_up(self):
        self._image = None
        self._segmentation_line = None
        self._pixel_path = None

    def split(self, image, segmentation_line):
        self._clean_up()
        self._image = image
        self._segmentation_line = segmentation_line
        self._split()

    def _split(self):
        pass

    @property
    def path(self):
        return self._pixel_path

class ForegroundPixelContourTracing(_AbstractImageSplitter):
    """Use foreground get_pixel contour tracing to split segment the image into two along the passed line."""

    def __init__(self, foreground_pixel_color=0, character_width=7,
                 distance_function=default_distance_function,
                 heuristic=default_heuristic,
                 neighbour_filter=default_neighbour_filter):
        super(ForegroundPixelContourTracing, self).__init__()
        self._foreground_pixel_color = foreground_pixel_color
        self._character_width = character_width
        self._distance_function = lambda origin, destination: distance_function(
            origin, destination,
            is_fully_accessible=destination.is_background_in(self._image),
            is_accessible_with_intersecting=destination.is_on(self._segmentation_line)
        )
        self._heuristic = lambda origin, destination: heuristic(origin, destination)
        self._neighbour_filter = lambda node: neighbour_filter(node, self._segmentation_line, self._character_width)

    def _split(self):
        start_pixel = Pixel(row=0, column=self._segmentation_line.x)
        end_pixel = Pixel(row=(self._image.height - 1), column=self._segmentation_line.x)
        self._pixel_path = PixelPath(AStar(image=self._image, start=start_pixel, goal=end_pixel,
                                           neighbour_filter=self._neighbour_filter,
                                           distance_function=self._distance_function,
                                           heuristic=self._heuristic).path)
        print('HI!')

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

if __name__ == '__main__':
    # image = Image(
    #     np.array([
    #         [1, 0, 1, 0, 0],
    #         [1, 1, 1, 0, 1],
    #         [1, 1, 0, 0, 1],
    #         [1, 1, 1, 1, 1]
    #     ], dtype=np.uint8) * 255,
    #     color_mode=ColorMode.binary
    # )

    image_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/word_2.png'
    image = Image.from_file(image_file)
    image = ToBinary().apply(image)

    segmentation_line = SegmentationLine(x=182)

    f = ForegroundPixelContourTracing()
    _ = f.split(image=image, segmentation_line=segmentation_line)
    pixel_path = f.path


    image = segmentation_line.paint_on(image, color=(255, 0, 0))
    image = pixel_path.paint_on(image, color=(0, 0, 255))
    image.show(wait_key=0)
