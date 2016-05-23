
import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy import cluster, linalg

from thresholdFilter import thresholdFilter

class characterFeatureExtraction:
	def __init__(self):
		self._th_fltr = thresholdFilter()

	def load_char(self, name):
		return cv2.imread(name,0)

	def clear_char(self, img):
		return self._th_fltr.global_threshold(img, 150, 1)

	def split_regions(self, img, R=3):
		return np.split(img, R, axis=1)

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
		print vector
		for r in range(len(img)):
			for c in xrange(1, len(img[r]), 1):
				if img[r][c-1] != img[r][c]:
					vector[r] = vector[r]+1

		return vector


	def invert_image(self, img):

		invert_fun = np.vectorize(self._invert_filter)

		return invert_fun(img)

	def _invert_filter(self, img):
		if img == 1:
			return 0
		return 1

if __name__ == '__main__':
	c = characterFeatureExtraction()

	tmp = c.clear_char(c.load_char("alpha1.png"))

	tmp = c.invert_image(tmp)

	regions = c.split_regions(tmp)

	#print c.horizontal_celled_prj_feature(regions)

	print c.crossing_feature(tmp)

	# x = cluster.vq.kmeans(cluster.vq.whiten(smth), 5)

	# print x

	plt.imshow(tmp, 'gray')
	plt.show()


