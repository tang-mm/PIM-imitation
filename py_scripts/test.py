#!/usr/bin/python

import numpy
import bob_gmm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


directory = '/media/winE/[TelecomParisTech]/Cours-3A/PIM-imitation/test/mfcc_full/'
# file name format: 'Gerra_to_Chirac_1.txt'
colors = ['r', 'b', 'g', 'y', 'c', 'm', 'orange', 'limegreen', 'navy','purple']
dict_speaker_points = {}

nb_cluster = 16
matrix = numpy.array([])
nb_file = 0

for file_matrix in os.listdir(directory):
	nb_file = nb_file + 1
	print file_matrix
	speaker = file_matrix.split('_')[2]	# get speaker name
	if speaker in dict_speaker_points:
		dict_speaker_points[speaker].append(nb_file)
	else:
		dict_speaker_points[speaker] = [nb_file]

print dict_speaker_points
