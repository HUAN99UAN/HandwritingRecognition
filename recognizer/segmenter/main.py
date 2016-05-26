import sys

# Fix path issues
from os.path import dirname, realpath
root = dirname(dirname(realpath(__file__)))
sys.path.append(root)

from inputOutput.openers import ImageOpener
from segmenter.lines import lineSegmenter


if __name__ == '__main__':
    image_path = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/segmenter/final.jpg'
    image = ImageOpener(image_file_path=image_path).open()
    l = lineSegmenter.LineSegmenter(image=image)
    l.segment()

    image = l.paint_stripes()
    image = l.paint_piece_wise_separating_lines(image)
    image.show()
