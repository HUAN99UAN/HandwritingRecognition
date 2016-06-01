import sys

# Fix path issues
from os.path import dirname, realpath
root = dirname(dirname(realpath(__file__)))
sys.path.append(root)

from inputOutput.openers import ImageOpener
from segmenter.lines import lineSegmenter
from segmenter.words.wordSegmenter import WordSegmenter

if __name__ == '__main__':
    image_path = '/Users/laura/Repositories/HandwritingRecognition/data/testdata/wordSegmenter/word.png'
    image = ImageOpener(image_file_path=image_path).open()


    parameters = {
        'white_threshold' : 240
    }

    w = WordSegmenter(word_image=image)
    w.segment()
    image.show()
