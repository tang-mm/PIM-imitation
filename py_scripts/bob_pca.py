#!/usr/bin/python

import numpy
import bob_gmm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


directory = '/media/winE/[TelecomParisTech]/Cours-3A/PIM-imitation/test/mfcc/'
# file name format: 'Gerra_to_Chirac_1.txt'

nb_cluster = 16
matrix = numpy.array([])
nb_file = 0

for file_matrix in os.listdir(directory):
	nb_file = nb_file + 1
	# read GMM means matrix (nb_clusters, 12) from each .wav 
	gmm = bob_gmm.get_gmm_model(nb_cluster, directory, file_matrix)
	# concatenate and form an overall matrix data of size ((nb_clusters * nb_files), 12)
	matrix = numpy.concatenate((matrix, gmm.means)) if matrix.size else gmm.means


# TODO: associate to a file name, concatenate all points of the same person. (using dictionary)


# ------- PCA training -------
data = matrix	# shape = (12 * (nb_cluster * nb_file))
print "\nNumber of files = ", nb_file
print "data size:", data.shape

pcaTrainer = bob.learn.linear.PCATrainer()
[pca_machine, eig_vals] = pcaTrainer.train(data)
print "PCA: weights shape", pca_machine.weights.shape
print "PCA: eig_vals\n", eig_vals


# ---------get first two dimensions -----------
two_dim_matrix = numpy.transpose(pca_machine.weights[:, [0,1]])  # first two columns with biggest eig_values, then transpose
print "two_dim", two_dim_matrix.shape

points = numpy.empty((nb_file, 2, nb_cluster)) # array of all point 2d-arrays
colors = ['r', 'b', 'g', 'y', 'c', 'm', 'k']

# plot points
for i in range(1, nb_file):
	segment = data[nb_cluster*(i-1): nb_cluster*i, :]
	print "segment shape ", segment.shape
	points[i-1] = numpy.dot(two_dim_matrix, numpy.transpose(segment))
	xs = points[i-1, 0]	# first line
	ys = points[i-1, 1]	# second line
	plt.scatter(xs, ys, c=colors[i-1], marker='s')
	
print "points: ", points
#points1 = numpy.dot(two_dim_matrix, numpy.transpose(data[[0,1,2,3], :])) # 2 * nb_cluster
#points2 = numpy.dot(two_dim_matrix, numpy.transpose(data[[4,5,6,7], :]))

# -------TEST----------- visualise --------
'''
fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

xs = points1[[0], :]
ys = points1[[1], :]
zs = [0,0,0,0]

xt = points2[[0], :]
yt = points2[[1], :]
zt = [0,0,0,0]

ax.scatter(xs, ys, zs, c='red', marker='o')
ax.scatter(xt, yt, zt, c='blue', marker='^')

ax.set_xlabel('X label')
ax.set_ylabel('Y label')
ax.set_zlabel('Z label')
'''
#plt.show()
#plt.plot(xs, ys, 'b^', xt, yt, 'rs')
plt.show()
