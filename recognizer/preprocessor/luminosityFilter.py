
import cv2
import numpy as np


class luminosityFilter:
	def __init__(self):
		pass

	def luminosity_normalization(self, img):
		size = img.shape
		y_center = size[0]/2
		x_center = size[1]/2
		center_sqr = img[y_center-500:y_center+500, x_center-500:x_center+500]
		lowest = center_sqr.min()
		highest = center_sqr.max()
		# lowest = img.min()
		# highest = img.max()
		# print lowest
		# print highest

		norm_f = np.vectorize(self._linear_norm)
		en_f = np.vectorize(self._linear_enhancement)

		new_img = norm_f(img.astype(int), lowest, highest)

		return new_img

	def _linear_norm(self, img, old_min_val, old_max_val, new_min_val = 0, new_max_val =255):
		return (img - old_min_val)*((new_max_val - new_min_val)/(old_max_val-old_min_val))+new_min_val

	def _linear_enhancement(self, img):
		return img*img*img

if __name__ == '__main__':
	img = cv2.imread("test2.jpg",0)
	l = luminosityFilter()

	l.luminosity_normalization(img)

