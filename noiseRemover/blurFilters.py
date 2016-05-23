import cv2
import numpy as np
from matplotlib import pyplot as plt

class blurFilters:
	def __init__(self):
		pass

	def gaussian_blur(self, img, size = (5,5)):
		return cv2.GaussianBlur(img,size,0)

	def median_blur(self, img, size = 5):
		return cv2.medianBlur(img,size)

	def simple_blur(self, img, mask):
		return cv2.filter2D(img,-1,mask)


if __name__ == '__main__':
	fltr = blurFilters()

	img = cv2.imread('test.jpg',0)

	mask = np.ones((5,5),np.float32)/25

	img_after_gaussian = fltr.gaussian_blur(img)
	img_after_median = fltr.median_blur(img)
	img_after_simple_blur = fltr.simple_blur(img, mask)

	images = [img, img_after_gaussian, img_after_median, img_after_simple_blur]

	titles = ['original', 'gaussian', 'median', 'simple']

	for i in xrange(4):
		plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
		plt.title(titles[i])
		plt.xticks([]),plt.yticks([])
	plt.show()