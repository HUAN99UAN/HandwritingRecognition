import cv2
import numpy as np
from matplotlib import pyplot as plt

from blurFilters import blurFilters

class gradientFilters:
	def __init__(self):
		pass

	def laplacian_filter(self, img):
		return cv2.Laplacian(img,cv2.CV_64F)

	def sobel_x(self, img, mask_size = 5):
		return cv2.Sobel(img,cv2.CV_64F,1,0,ksize=mask_size)

	def sobel_y(self, img, mask_size = 5):
		return cv2.Sobel(img,cv2.CV_64F,0,1,ksize=mask_size)

if __name__ == '__main__':
	fltr = gradientFilters()
	blr_fltr = blurFilters()

	img = cv2.imread('test.jpg',0)
	img = blr_fltr.median_blur(img)

	images = [img, fltr.laplacian_filter(img), fltr.sobel_x(img), fltr.sobel_y(img)]

	titles = ['original', 'laplacian', 'sobel x', 'sobel y']

	for i in xrange(4):
		plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
		plt.title(titles[i])
		plt.xticks([]),plt.yticks([])
	plt.show()