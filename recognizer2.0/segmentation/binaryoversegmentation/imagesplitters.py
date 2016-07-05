import sys
import copy

import numpy as np

from segmentation.binaryoversegmentation.astar import AStar
from utils.things import Pixel, PixelPath, BoundingBox
from utils.image import Image, ColorMode
from segmentation.binaryoversegmentation.segmentationlines import SegmentationLine
from utils.mixins import CommonEqualityMixin
from utils.shapes import Rectangle
from utils.things import Point

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


class _AbstractImageSplitter(CommonEqualityMixin):

    def __init__(self, background_color=255, foreground_color=0):
        self._image = None
        self._segmentation_line = None
        self._pixel_path = None

        self._foreground_pixel_color = foreground_color
        self._background_color = background_color

    def _clean_up(self):
        self._image = None
        self._segmentation_line = None
        self._pixel_path = None

    def split(self, image, segmentation_line):
        self._clean_up()
        self._image = image
        self._segmentation_line = segmentation_line
        return self._split()

    def _split(self):
        pass

    def _split_images(self):
        return self._left_image(), self._right_image()

    def _pixels_on_one_side_of_pixel_path(self, getter):
        pixels = set() #Don't use a list, you'll get duplicate pixels.
        for pixel in self._pixel_path:
            new_pixels = getter(pixel, self._image)
            pixels.update(new_pixels)
        return zip(*pixels)

    def _set_to_background(self, x_coordinates, y_coordinates):
        image_copy = copy.deepcopy(self._image)
        image_copy[x_coordinates, y_coordinates] = self._background_color
        return image_copy

    def _right_image(self):
        (x_coordinates, y_coordinates) = self._pixels_on_one_side_of_pixel_path(Pixel.pixels_left_of_in)
        image = self._set_to_background(x_coordinates, y_coordinates)
        bounding_box = BoundingBox(
            top=0, bottom=self._image.height - 1,
            left=self._pixel_path.min_column_idx, right=self._image.width - 1
        )
        return image.sub_image(bounding_box=bounding_box)

    def _left_image(self):
        (x_coordinates, y_coordinates) = self._pixels_on_one_side_of_pixel_path(Pixel.pixels_right_of_in)
        image = self._set_to_background(x_coordinates, y_coordinates)
        bounding_box = BoundingBox(
            top=0, bottom=self._image.height - 1,
            left=0, right=self._pixel_path.max_column_idx
        )
        return image.sub_image(bounding_box=bounding_box)

    @property
    def path(self):
        return self._pixel_path


class StraightLineSplitter(_AbstractImageSplitter):
    def __init__(self, background_color=255, foreground_color=0):
        super(StraightLineSplitter, self).__init__(background_color, foreground_color)

    def _split(self):
        left_bounding_box = Rectangle(corner=Point(x=0, y=0), opposite_corner=Point(x=self._segmentation_line.x, y=self._image.height - 1))
        left_sub_image = self._image.sub_image(left_bounding_box, remove_white_borders=False)

        right_bounding_box = Rectangle(corner=Point(x=self._segmentation_line.x, y=0), opposite_corner=Point(x=self._image.width -1, y=self._image.height -1))
        right_sub_image = self._image.sub_image(right_bounding_box, remove_white_borders=False)

        return left_sub_image, right_sub_image


class ForegroundPixelContourTracing(_AbstractImageSplitter):
    """Use foreground get_pixel contour tracing to split segment the image into two along the passed line."""

    def __init__(self, character_width=7,
                 distance_function=default_distance_function,
                 heuristic=default_heuristic,
                 neighbour_filter=default_neighbour_filter):
        super(ForegroundPixelContourTracing, self).__init__()
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
        return self._split_images()

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

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

    image_file = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/segmentation_image.pkl'
    with open(image_file, 'r') as input:
        import pickle
        image = pickle.load(input)

    segmentation_line = SegmentationLine(x=182)

    f = ForegroundPixelContourTracing()
    left, right = f.split(image=image, segmentation_line=segmentation_line)

    print('HI!')

    # right.resize(height=400).show(window_name='Right', wait_key=0)
    # left.resize(height=400).show(window_name='Left', wait_key=0)
    #
    # image = segmentation_line.paint_on(image, color=(255, 0, 0))
    # image = pixel_path.paint_on(image, color=(0, 0, 255))
    # image.resize(height=400).show(wait_key=0)
