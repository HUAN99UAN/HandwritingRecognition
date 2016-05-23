
import cv2
import numpy as np
from matplotlib import pyplot as plt

from gradientFilters import gradientFilters
from thresholding import thresholdFilter

from morphologicalFilters import morphologicalFilters
from edgeFilter import edgeFilter
from segmentationFilter import segmentationFilter
from interpolationFilter import interpolationFilter

class removeNoisePipe:




	def _closing_by_reconstruction(self, img, dilation_mask = (7,7), erosion_mask = (3,3)):
		img_after_threshold = self._th_fltr.global_threshold(img.astype(np.uint8),170,255) #value of thresshold - value to be replaces
		
		img_dil = self._morph_fltr.dilation(img_after_threshold, dilation_mask)

		tmp_img = np.copy(img_dil)

		for i in xrange(100):
			tmp_img = self._morph_fltr.erosion(tmp_img, erosion_mask)
			tmp_img = np.maximum(tmp_img, img_after_threshold)

		return tmp_img

	


if __name__ == '__main__':
	rmv_noise = removeNoisePipe()
	img = cv2.imread('test.jpg', 0)


	#img = np.array([1,2,3,4,5])

	# hist = np.sum(img, axis=0)
	# print "min: ", hist.min()
	# print "max: ", hist.max()
	# print "mean: ", np.mean(hist)
	# print "median: ", np.median(hist)

	# hist = np.sum(img, axis=1)
	# print "min: ", hist.min()
	# print "max: ", hist.max()
	# print "mean: ", np.mean(hist)
	# print "median: ", np.median(hist)
	# y = np.sin(hist)
	# plt.plot(hist)
	# plt.show()
	img_after_norm = rmv_noise._luminosity_normalization(img)

	img_after_noise_removal = rmv_noise._openning_by_reconstruction(img_after_norm)

	cv2.imwrite("reco.jpg", img_after_noise_removal)

	#cv2.imwrite("op_n_rec.jpg", rmv_noise._remove_noise_pipe(img))

