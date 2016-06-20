import interface
import numpy as np


class CellProjection(interface.AbstractFeatureExtractor):
    def __init__(self):
        super(CellProjection, self).__init__()

    @staticmethod
    def _split_regions(img, regions=4, axis=1):
        return np.split(img, regions, axis=axis)

    @staticmethod
    def _invert_image(img):
        return (img == 0).astype(int)

    @staticmethod
    def _concat(matrix):
        return matrix.ravel()

    def extract(self, image):
        regions = self._split_regions(image)
        feature_matrix = self._horizontal_celled_prj_feature(regions)
        return self._concat(feature_matrix)


    def _horizontal_celled_prj_feature(self, regions):

        total_rows = 0
        counter = 0

        for r in regions:
            total_rows += len(r)

        vector = np.zeros(total_rows)

        for r in regions:
            for row in r:
                for c in row:
                    if c == 1:
                        vector[counter] = 1
                        break
                counter += 1

        return vector.reshape(len(regions), total_rows / len(regions))


if __name__ == '__main__':
    matrix = [[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
              ]

    c = CellProjection()
    print c.extract(np.array(matrix))
