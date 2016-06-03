

import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy import cluster, linalg
from PIL import Image

from thresholdFilter import thresholdFilter

class characterFeatureExtraction:
	def __init__(self):
		self._th_fltr = thresholdFilter()

	def load_char(self, name):
		return Image.open(name).convert('L')

	def clear_char(self, img):
		return self._th_fltr.global_threshold(img, 150, 1)

	def split_regions(self, img, R=4):
		return np.split(img, R, axis=1)

	def resize_img(self, img):
		return img.resize((128,128), Image.BILINEAR)

	def horizontal_celled_prj_feature(self, regions):

		total_rows = 0
		counter = 0

		for r in regions:
			total_rows = total_rows + len(r)
		 
		vector = np.zeros(total_rows)

		for r in regions:
			for row in r:
				for c in row:
					if c == 1:
						vector[counter] = 1
						break
				counter = counter + 1

		return vector.reshape(len(regions),total_rows/len(regions))

	def crossing_feature(self, img):
		size = img.shape

		vector = np.zeros(size[0])
		for r in range(len(img)):
			for c in xrange(1, len(img[r]), 1):
				if img[r][c-1] != img[r][c]:
					vector[r] = vector[r]+1

		return vector

	def hist_feature(self, img):
		hist_y = np.sum(img, axis=1)
		hist_x = np.sum(img, axis=0)

		return {'hist_x': hist_x, 'hist_y': hist_y}


	def invert_image(self, img):

		invert_fun = np.vectorize(self._invert_filter)

		return invert_fun(img)

	def _invert_filter(self, img):
		if img == 1:
			return 0
		return 1

if __name__ == '__main__':
	c = characterFeatureExtraction()

	tmp = c.load_char("Selection_024.png")
	tmp = c.resize_img(tmp)
	img = np.asarray(tmp)
	img = c.clear_char(img)
	tmp2 = c.invert_image(img)
	regions = c.split_regions(tmp2)

	for i in regions[1]:
		print i

	# hog = cv2.HOGDescriptor()
	# h = hog.compute(img, (8,8))
	# print h.shape
	# pca = cv2.PCACompute(h, np.mean(h, axis=0).reshape(1,-1), 10)

	# print type(pca)

	# print pca

	# print c.horizontal_celled_prj_feature(regions)

	# print c.crossing_feature(img)

	#data = c.hist_feature(tmp)

	# print x

	# plt.imshow(tmp, 'gray')
	# plt.show()
