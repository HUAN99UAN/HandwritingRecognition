
import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy import cluster, linalg

from thresholdFilter import thresholdFilter

class characterFeatureExtraction:
	def __init__(self):
		self._th_fltr = thresholdFilter()

	def load_char(self):
		return cv2.imread("alpha1.png",0)

	def clear_char(self, img):
		return self._th_fltr.global_threshold(img, 150, 1)

	def split_regions(self, img, R=3):
		return np.split(img, R, axis=1)

	def horizontal_celled_prj_feature(self, regions, rows):
		 
		vector = np.zeros(rows*len(regions))
		counter = 0

		for r in regions:
			for row in r:
				for c in row:
					if c == 1:
						vector[counter] = 1
						break
				counter = counter +1

		return vector.reshape(3,51)

	def invert_image(self, img):

		invert_fun = np.vectorize(self._invert_filter)

		return invert_fun(img)

	def _invert_filter(self, img):
		if img == 1:
			return 0
		return 1

if __name__ == '__main__':
	c = characterFeatureExtraction()

	tmp = c.clear_char(c.load_char())

	z = np.ones((51,1))

	for i in xrange(6):
		tmp = np.append(tmp, z, axis=1)

	tmp = c.invert_image(tmp)

	regions = c.split_regions(tmp)

	print c.horizontal_celled_prj_feature(regions, tmp.shape[1])

	# x = cluster.vq.kmeans(cluster.vq.whiten(smth), 5)

	# print x

	# plt.imshow(tmp, 'gray')
	# plt.show()


