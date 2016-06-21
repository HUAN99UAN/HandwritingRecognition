import interface
import cv2
import numpy as np
from matplotlib import pyplot

class StupidSegmentation(interface.AbstractSegmenter):

    def __init__(self):
        super(StupidSegmentation, self).__init__()

    def get_img(self, img):
        img = cv2.imread(img, 0)
        height = img.shape[0]
        width = img.shape[1]
        _, image = cv2.threshold(img, thresh=0, maxval=255, type=cv2.THRESH_OTSU+cv2.THRESH_BINARY)

        hist = self.create_hist(image)
        points = self.find_valleys(hist)

        print hist
        print points


        for point in points:
             cv2.line(image, (point, 0), (point, 100), (0, 255, 255), thickness=1, lineType=8, shift=0)

        pyplot.imshow(image, 'gray')
        pyplot.show()
        points = np.insert(points, 0, 0)
        points = np.append(points, width)
        for idx in range(len(points)-2): # img[200:400, 100:300] # Crop from x, y, w, h
             mask = image[0:height, points[idx]:points[idx+2]]
             pyplot.imshow(mask, 'gray')
             pyplot.show()
             mask = image[0:height, points[idx]:points[idx+1]]
             pyplot.imshow(mask, 'gray')
             pyplot.show()


        # cv2.imshow('image', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def find_valleys(self, hist):
        window_size = 16
        minima = []
        for i in range(window_size, len(hist)-window_size, window_size):
            tmp_max = i
            for x in range(i-window_size/2, i+window_size/2):
                if hist[x] > hist[i]:
                    tmp_max = x
            minima.append(tmp_max)

        return np.unique(minima)

    def create_hist(self, img):
        hist = []
        #print img
        for col in img.T:
            hist.append(sum(col))
        # pyplot.plot(np.asarray(hist))
        # pyplot.show()
        return np.asarray(hist)







if __name__ == '__main__':
    r = StupidSegmentation()
    r.get_img('Selection_001.png')
