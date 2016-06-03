
import cv2
import numpy as np
from matplotlib import pyplot as plt

from thresholdFilter import thresholdFilter

class wordProcessing:
	def __init__(self):
		self._th_fltr = thresholdFilter()
		self._array_of_pos = []

	def load_word(self, name):
		return cv2.imread(name,0)

	def clear_word(self, img):
		return self._th_fltr.global_threshold(img, 70, 1)

	def find_local_minima(self, hist):
		for pos in xrange(3,len(hist)-3,1):
			if hist[pos] > np.max(hist[pos-3:pos]) and hist[pos] > np.max(hist[pos+1:pos+3]):
				self._array_of_pos.append(pos)

		return self._array_of_pos


if __name__ == '__main__':
	w = wordProcessing()

	img = w.load_word('word.png')
	img = w.clear_word(img)

	hist = img.sum(axis = 0)

	mean = np.mean(hist)
	m = np.min(hist)
	print m
	print mean
	print w.find_local_minima(hist)

	print img.sum(axis=0)

	plt.plot(img.sum(axis=0), 'r')
	plt.imshow(img, 'gray')
	plt.show()


