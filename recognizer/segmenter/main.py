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


    parameters = {
        'white_threshold' : 240
    }

    # TODO: Draw the found baseline

    w = WordSegmenter(word_image=image, parameters=parameters)
    w.segment()
    image.show()
