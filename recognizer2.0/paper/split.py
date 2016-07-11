import os.path

from utils.image import Image
import utils.colors as colors
from preprocessing.colorspaces import ToBinary
from segmentation.binaryoversegmentation.segmentationlines import  SegmentationLine
from segmentation.binaryoversegmentation.imagesplitters import StraightLineSplitter, ForegroundPixelContourTracing

wd = '/Users/laura/Repositories/HandwritingRecognition/report/shared/img/method'


def split_along_straight_line(image, line):
    binary_image = ToBinary().apply(image)
    left, right = StraightLineSplitter().split(binary_image, line)

    output_image = line.paint_on(image, color=colors.yellow)
    output_image = line.paint_on(output_image, color=colors.red)
    output_image.to_file(os.path.join(wd, 'split_straight_path.png'))

    left.to_file(os.path.join(wd, 'split_straight_left.png'))
    right.to_file(os.path.join(wd, 'split_straigt_right.png'))


def split_along_a_star_path(image, line):
    binary_image = ToBinary().apply(image)

    path, (left, right) = ForegroundPixelContourTracing(return_path=True).split(binary_image, line)

    output_image = line.paint_on(image, color=colors.yellow)
    output_image = path.paint_on(output_image, color=colors.red)
    output_image.to_file(os.path.join(wd, 'split_astar_path.png'))

    left.to_file(os.path.join(wd, 'split_astar_left.png'))
    right.to_file(os.path.join(wd, 'split_astar_right.png'))


if __name__ == '__main__':
    image_file = os.path.join(wd, 'split_basic_image.png')
    image = Image.from_file(image_file)

    segmentation_line = SegmentationLine(x=38)

    split_along_a_star_path(image, segmentation_line)
    split_along_straight_line(image, segmentation_line)

