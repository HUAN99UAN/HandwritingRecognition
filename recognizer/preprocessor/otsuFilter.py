import cv2
import numpy as np

class otsuFilter:
	def __init__(self):
		pass

	def otsu_threshold(self, img, threshold = 0):
		img_grey = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2GRAY)
		_, img_after_otsu = cv2.threshold(img_grey,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		return img_after_otsu

if __name__ == '__main__':
	fltr = otsuFilter()

	img = cv2.imread('test.jpg',0)

	img_after_otsu = fltr.otsu_threshold(img)


	cv2.imwrite('otsu.jpg', img_after_otsu)
	plt.imshow(img_after_otsu, 'gray')
	plt.show()