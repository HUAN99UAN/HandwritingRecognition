import cv2
import numpy as np
from matplotlib import pyplot as plt

from blurFilters import blurFilters
from thresholding import thresholdFilter
from morphologicalFilters import morphologicalFilters

mf = morphologicalFilters()
bf = blurFilters()
tf = thresholdFilter()

img = cv2.imread('test.jpg',0)

img1 = bf.simple_blur(img, np.ones((7,7),np.float32)/49)

img2 = tf.adaptive_gaussian_threshold(img1)

img3 = mf.openning(img2, np.ones((5,5),np.uint8))

images = [img, img3]

titles = ['original', 'thres after blur']

for i in xrange(2):
	plt.subplot(2,1,i+1),plt.imshow(images[i],'gray')
	plt.title(titles[i])
	plt.xticks([]),plt.yticks([])
plt.show()