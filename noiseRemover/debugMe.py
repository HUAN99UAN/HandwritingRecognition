
import numpy as np

from matplotlib import pyplot as plt

def plot_me(img):
	plt.imshow(img, 'gray')
	plt.show()

def print_me(img):
	print "max: ", img.max()
	print "min: ", img.min()
	print img.shape
	print img.dtype

def plot_us(imgs):


	for i in xrange(len(imgs)):
		plt.subplot(2,2,i+1),plt.imshow(imgs[i],'gray')
		plt.xticks([]),plt.yticks([])
	plt.show()

