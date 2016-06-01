from segmenter.words.SuspiciousSegmentationPointGenerator import SuspiciousSegmentationPointGenerator

class WordSegmenter:

    def __init__(self, word_image):
        self._word_image = word_image

    def segment(self):
        ssps = SuspiciousSegmentationPointGenerator(image=self._word_image)
