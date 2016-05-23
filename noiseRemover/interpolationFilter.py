
import cv2
import numpy as np
from matplotlib import pyplot as plt

class interpolationFilter:
	def __init__(self):
		pass

	def fast_marching_telea(self, img, mask):
		return cv2.inpaint(img,mask,3,cv2.INPAINT_TELEA)


	def fast_marching_ns(self, img, mask):
		return cv2.inpaint(img,mask,3,cv2.INPAINT_NS)

if __name__ == '__main__':
	inter_fltr = interpolationFilter()
	mask = cv2.imread("mask.jpg", 0)
	img = cv2.imread("otsu_closing5.jpg")

	final_image = inter_fltr.fast_marching_telea(img,mask)

	cv2.imwrite("ns.jpg", final_image)
