
import cv2
import numpy as np
from matplotlib import pyplot as plt

from morphologicalFilters import morphologicalFilters
from luminosityFilter import luminosityFilter
from thresholdFilter import thresholdFilter
from imageSquerify import imageSquerify
import debugMe

class pipe:
	def __init__(self):
		self._morph_fltr = morphologicalFilters()
		self._lum_fltr = luminosityFilter()
		self._th_fltr = thresholdFilter()
		self._img_sqr = imageSquerify()

	def pipe_line(self, img):


		img_after_lum_norm = self._lum_fltr.luminosity_normalization(img)


		img_after_threshold = self._th_fltr.global_threshold(img_after_lum_norm.astype(np.uint8), 150, 1)

		
		img_after_closing = self._morph_fltr.openning(img_after_threshold.astype(np.uint8), (3,3))


		img_after_open_reco = self._morph_fltr.openning_by_reconstruction(img_after_closing)


		#img_after_border_rmv = self._img_sqr.rmv_borders(img_after_open_reco)

		return img_after_open_reco

	def tmp(self,img):
		#return self._img_sqr.lauras_function(img)
		#return self._img_sqr.rmv_borders(img)
		return self._img_sqr.crop_pipe(img)


if __name__ == '__main__':
	p = pipe()

	img = cv2.imread("test.jpg", 0)

	img2 = p.pipe_line(img)

	img3 = p.tmp(img2.astype(np.uint8))
	#debugMe.print_me(img2)

	plt.imshow(img3, 'gray')
	plt.show()

