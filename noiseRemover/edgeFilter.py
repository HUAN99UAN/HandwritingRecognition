
import cv2
import numpy as np
from matplotlib import pyplot as plt

class edgeFilter:

	def __init__(self):
		pass

	def canny_edges(self, img, low = 25, high = 50):
		return cv2.Canny(img,low,high)


if __name__ == '__main__':
	fltr = edgeFilter()

	img = cv2.imread('test.jpg',0)

	img_canny_edged = fltr.canny_edges(img)

	images = [img, fltr.canny_edges(img,0,100), fltr.canny_edges(img, 100, 200), fltr.canny_edges(img,0,500), fltr.canny_edges(img,400,500), fltr.canny_edges(img,5,10)]

	titles = ['original', 'canny 0-100', 'canny 100-200', 'canny 0-500', 'canny 400-500', 'canny 5-10']


	for i in xrange(6):
		plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
		plt.title(titles[i])
		plt.xticks([]),plt.yticks([])
	plt.show()
