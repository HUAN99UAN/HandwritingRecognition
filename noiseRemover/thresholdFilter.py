
import cv2
import numpy as np
from matplotlib import pyplot as plt

from blurFilters import blurFilters


class thresholdFilter:
	def __init__(self):
		pass

	def global_threshold(self, img, threshold = 200, max_val = 1):
		garbage, img = cv2.threshold(img,threshold,max_val,cv2.THRESH_BINARY)
		return img

	def adaptive_mean_threshold(self, img):
		return cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
		cv2.THRESH_BINARY,11,2)

	def adaptive_gaussian_threshold(self, img):
		return cv2.adaptiveThreshold(img,100,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
			cv2.THRESH_BINARY,11,2)

if __name__ == '__main__':
	fltr = thresholdFilter()
	blr_fltr = blurFilters()

	img = cv2.imread('test.jpg',0)
	img = blr_fltr.median_blur(img)

	#garbage,global_th = fltr.gobal_threshold(img)
	images = [img, fltr.global_threshold(img, 170, 1), fltr.global_threshold(img, 180, 1), fltr.global_threshold(img,190,1)]

	titles = ['original', 'global thres',
			'adaptive median thres', 'adaptive gaussian thres']

	for i in xrange(4):
		plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
		plt.title(titles[i])
		plt.xticks([]),plt.yticks([])
	plt.show()