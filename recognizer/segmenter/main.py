import sys

import numpy as np

# Fix path issues
from os.path import dirname, realpath
root = dirname(dirname(realpath(__file__)))
sys.path.append(root)

from inputOutput.openers import ImageOpener
from segmenter.words.wordSegmenter import WordSegmenter
import segmenter.words.SuspiciousSegmentationPointGenerator as ssp_generator

if __name__ == '__main__':
    image_path = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/wordSegmenter/word.png'
    image = ImageOpener(image_file_path=image_path).open()


    # parameters = {
    #     'white_threshold' : 240
    # }

    # TODO: Move default parameters to wordSegmenter.
    # TODO: Baseline computation fails with actual image
    # TODO: Draw the found baseline

    # image = np.array([[0, 0, 1, 0, 0, 0], [1, 1, 1, 0, 1, 1], [1, 1, 0, 1, 0, 0], [0, 1, 1, 1, 1, 0]])
    # ssp_generator._BaseLineComputer(foreground=image).compute()

    w = WordSegmenter(word_image=image)
    w.segment()
    image.show()
