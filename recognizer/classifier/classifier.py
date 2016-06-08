from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib.pyplot as plt



class classifier:
	def __init__(self):
		pass

	def knn(self, dataset):

		X = np.array(dataset)
		nbrs = NearestNeighbors(n_neighbors=27, algorithm='ball_tree').fit(X) # kd_tree
		distances, indices = nbrs.kneighbors(X)
		return distances, indices #  
		#print indices

if __name__ == '__main__':

	c = classifier()
	

	with open("test.txt",'r') as f_handle:
		l = np.loadtxt(f_handle)

	D, I = c.knn(np.split(l, 128))

	for i in range(len(D)):
		plt.scatter(I[i], D[i])
	plt.show()

	# fig = plt.figure(figsize=(6, 3.2))

	# ax = fig.add_subplot(111)
	# ax.set_title('colorMap')
	# plt.imshow(H)
	# ax.set_aspect('equal')

	# cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
	# cax.get_xaxis().set_visible(False)
	# cax.get_yaxis().set_visible(False)
	# cax.patch.set_alpha(0)
	# cax.set_frame_on(False)
	# plt.colorbar(orientation='vertical')
	# plt.show()