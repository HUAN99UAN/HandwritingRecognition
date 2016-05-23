import cv2
import numpy as np
from matplotlib import pyplot as plt

class segmentationFilter:
	def __init__(self):
		pass

	def watershed(self, img):

		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

		garbage, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

		return thresh


if __name__ == '__main__':
	fltr = segmentationFilter()

	img = cv2.imread('test.jpg')

	img_after_watershed = fltr.watershed(img)

	images = [img, img_after_watershed]

	titles = ['original', 'watershed']

	for i in xrange(2):
		plt.subplot(2,1,i+1),plt.imshow(images[i],'gray')
		plt.title(titles[i])
		plt.xticks([]),plt.yticks([])
	plt.show()
