
import cv2
import numpy as np
from matplotlib import pyplot as plt

from thresholdFilter import thresholdFilter

class morphologicalFilters:

	def __init__(self):
		self._th_fltr = thresholdFilter()

	def erosion(self, img, mask):
		return cv2.erode(img,np.ones(mask,np.uint8),iterations = 1)

	def dilation(self, img, mask):
		return cv2.dilate(img,np.ones(mask,np.uint8),iterations = 1)

	def openning(self, img, mask):
		return cv2.morphologyEx(img, cv2.MORPH_OPEN, np.ones(mask,np.uint8))

	def closing(self, img, mask):
		return cv2.morphologyEx(img, cv2.MORPH_CLOSE, np.ones(mask,np.uint8))

	def openning_by_reconstruction(self, img, dilation_mask = (7,7), erosion_mask = (3,3)):	
		img_dil = self.dilation(img, dilation_mask)

		tmp_img = np.copy(img_dil)

		for i in xrange(100):
			tmp_img = self.erosion(tmp_img, erosion_mask)
			tmp_img = np.maximum(tmp_img, img)

		return tmp_img

	def closing_by_reconstruction(self, img, dilation_mask = (3,3), erosion_mask = (3,3)):
		img_ero = self.erosion(img, erosion_mask)

		tmp_img = np.copy(img_ero)

		# for i in xrange(100):
		# 	tmp_img = self.dilation(tmp_img, dilation_mask)
		# 	tmp_img = np.minimum(tmp_img, img)

		return tmp_img

if __name__ == '__main__':
	fltr = morphologicalFilters()

	img = cv2.imread('test.jpg',0)

	mask = np.ones((5,5),np.uint8)

	images = [img, fltr.erosion(img, mask), fltr.dilation(img, mask), fltr.openning(img, mask), fltr.closing(img, mask)]

	titles = ['original', 'eroded', 'dilated', 'opened', 'closed']

	for i in xrange(5):
		plt.subplot(3,3,i+1),plt.imshow(images[i],'gray')
		plt.title(titles[i])
		plt.xticks([]),plt.yticks([])
	plt.show()

