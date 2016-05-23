

import cv2
import numpy as np
from matplotlib import pyplot as plt

from morphologicalFilters import morphologicalFilters
from thresholding import thresholdFilter
from otsuFilter import otsuFilter
from blurFilters import blurFilters
import debugMe

class imageSquerify:
	def __init__(self):
		self._morph_fltr = morphologicalFilters()
		self._th_fltr = thresholdFilter()
		self._otsu_fltr = otsuFilter()
		self._blur_fltr = blurFilters()


	def _lauras_function(self, img):
		img_blurred = self._blur_fltr.gaussian_blur(img)
		img_otsu = self._otsu_fltr.otsu_threshold(img_blurred)
		img_final = self._morph_fltr.erosion(img_otsu, (40,40))

		return img_final


	def rmv_borders(self, img):
		mask = self._create_mask(img)

		tmp_img = self._morph_fltr.openning_by_reconstruction(img, (20,20), (10,10))
		
		fun = np.vectorize(self._my_fun)
		
		for i in range(50):
		 	mask = self._morph_fltr.dilation(mask, (10,10))
		 	new_img = fun(mask, tmp_img)
			
		asdf = np.maximum(img, new_img)
		
		return asdf

	def _create_mask(self, img):
		mask = np.zeros(img.shape)
		return self._create_borders_for_mask(mask)

	def _create_borders_for_mask(self, mask):
		mask[0,:] = 1
		mask[:,0] = 1
		mask[-1,:] = 1
		mask[:,-1] = 1
		return mask

	def _my_fun(self, mask, img):
		if mask == 1 and img == 0:
			return 1
		else:
			return 0

	def _get_hist(self,img,axis=0):
		return {'x-axis': img.sum(axis=0), 'y-axis': img.sum(axis=1)}

	def _find_peaks(self, hist, step = 100):
		low = np.amin(hist)
		high = np.amax(hist)
		avrg = (high+low)/2
		low_avrg = avrg-avrg*0.2
		high_avrg = avrg+avrg*0.2

		print low
		print high
		print avrg
		print low_avrg
		print high_avrg

		hist = hist.astype(int)

		start = end = 0

		for i in xrange(0, len(hist)-step, step):
			if hist[i] - hist[i+step] > avrg:
				start = i
				break

		for i in xrange(start+step, len(hist)-step, step):
			print "i: ", i
			print "diff: ", hist[i] - hist[i+step]
			if (hist[i] - hist[i+step] < -low_avrg) and (hist[i] - hist[i+step] > -high_avrg):
				end = i
				print "!!!"
				break
		
		return {'start': start, 'end': end}

	def _crop(self, img, x_borders, y_borders):
		window = img[	y_borders['start']:y_borders['end']+100,
						x_borders['start']:x_borders['end']+100]
		return window

	def crop_pipe(self,img):
		bolded_img = self._lauras_function(img)
		hist_data = self._get_hist(bolded_img)
		#plt.imshow(bolded_img, 'gray')
		#plt.show()
		#plt.plot(hist_data['x-axis'])
		#plt.show()
		plt.plot(hist_data['y-axis'])
		plt.show()

		x_borders = self._find_peaks(hist_data['x-axis'])

		y_borders = self._find_peaks(hist_data['y-axis'])
		print x_borders
		print "+++++"
		print y_borders

		return self._crop(img, x_borders, y_borders)

if __name__ == '__main__':
	im_sqr = imageSquerify()
	img = cv2.imread("test.jpg", 0)
	new_img = im_sqr.crop_pipe(img)

	plt.imshow(new_img, 'gray')
	plt.show()

	
