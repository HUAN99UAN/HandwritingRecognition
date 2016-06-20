import interface
import numpy as np


class SimplePixels(interface.AbstractFeatureExtractor):
    def __init__(self):
        super(SimplePixels, self).__init__()

    def _invert_image(self, image):
        return super(SimplePixels, self)._invert_image(image)

    def _concat(self, image):
        return super(SimplePixels, self)._concat(image)

    def extract(self, image):
        inverted_image = self._invert_image(image)
        return self._concat(image)

if __name__ == '__main__':
    matrix = [[0, 0, 0, 1],
              [0, 0, 1, 0],
              [0, 1, 0, 0]
              ]


    s = SimplePixels()
    print s.extract(np.array(matrix))