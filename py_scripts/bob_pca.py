#!/usr/bin/python

import numpy
import bob_gmm, bob.learn.linear
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


# form overall matrix for all speakers
def get_matrix_all_speakers(nb_cluster, directory, datatype, is_same_speaker):
    if datatype.lower() not in ['mfcc', 'pitch', 'formant']:
        raise ValueError('Error: data type must be \'mfcc\', \'pitch\' or \'formant\'!')

    matrix = numpy.array([])
    nb_file = 0
    dict_speaker_points = {}

    for file_matrix in sorted(os.listdir(directory)):   # sort filenames in order to maintain the same reading order
        nb_file = nb_file + 1
        
        # get speaker name
        if is_same_speaker: # one speaker imitating N persons
            speaker = file_matrix.split('_')[2] # ex. Gerra_to_Sarkozy_1.txt  --> Sarkozy
        else:
            speaker = file_matrix.split('_')[0] # ex. Gerra_to_Sarkozy_1.txt --> Gerra; Sarkozy_1.txt
                 
        # associate files to speaker name in order of reading
        if speaker in dict_speaker_points:
            if nb_file not in dict_speaker_points[speaker]:
                dict_speaker_points[speaker].append(nb_file)
        else:
    		dict_speaker_points[speaker] = [nb_file]
   
        # read GMM means matrix (nb_clusters, 12) from each .wav 
        gmm = bob_gmm.get_gmm_model(nb_cluster, directory, file_matrix, datatype)
        # concatenate and form an overall matrix data of size ((nb_clusters * nb_files), 12)
        matrix = numpy.concatenate((matrix, gmm.means)) if matrix.size else gmm.means

    return matrix, nb_file, dict_speaker_points


# reduce MFCC matrix dimension: PCA training 
def get_reduced_matrix_pca(matrix, nb_cluster, directory):
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

    return two_dim_matrix

# --------visualization MFCC -----------
def visualize_mfcc_2D(data, two_dim_matrix, nb_file, dict_speaker_points, legend_title):
    colors = ['r', 'b', 'g', 'y', 'c', 'm', 'orange', 'navy', 'purple', 'limegreen']
    my_marker = '+'
    
    fig = plt.figure()
    ax = plt.subplot(111) 	# projection = 3d
    
    points = numpy.empty((nb_file, 2, nb_cluster)) # array of all point 2d-arrays
    count = 0
    # plot points
    for speaker in dict_speaker_points:
	# get points in all files of this speaker
        file_number = dict_speaker_points[speaker]
        xx = []
        yy = []
        for i in file_number:
            segment = data[nb_cluster*(i-1): nb_cluster*i, :]	# lines corresponding to each file
            points[i-1] = numpy.dot(two_dim_matrix, numpy.transpose(segment))
            xs = points[i-1, 0]	# first line --> x
            ys = points[i-1, 1]	# second line --> y
            xx.extend(xs)	# append all points of this speaker
            yy.extend(ys)
        
        ax.scatter(xx, yy, c=colors[count], marker=my_marker, label=speaker)
        count = count+1
        print speaker, "\nXX:\n", xx
        print speaker, "\nYY:\n", yy
    
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    
    # add legend
    legend = ax.legend(loc='center left', title=legend_title, bbox_to_anchor=(1, 0.5), fontsize='small')
    legend.get_frame().set_facecolor=('silver')
    
    fig.savefig('image_output.png', dpi=300, format='png', bbox_extra_artists=(legend,), bbox_inches='tight')
    plt.show()


# get allover matrix of pitch and 2 formants: 1st colomn = pitch, 2nd / 3rd colomn = formant1/2
def get_matrix_pitch_formant(nb_cluster, dir_pitch, dir_formant1, dir_formant2, is_same_speaker):
    mat_pitch, nb_file1, dict_speaker_points1 = get_matrix_all_speakers(nb_cluster, dir_pitch, 'pitch', is_same_speaker)
    mat_f1, nb_file2, dict_speaker_points2 = get_matrix_all_speakers(nb_cluster, dir_formant1, 'formant', is_same_speaker)
    mat_f2, nb_file3, dict_speaker_points3 = get_matrix_all_speakers(nb_cluster, dir_formant2, 'formant', is_same_speaker)
    print mat_pitch.shape, mat_f1.shape, mat_f2.shape
    
    # check if the reading orders are the same
    if nb_file1 == nb_file2 == nb_file3 and dict_speaker_points1 == dict_speaker_points2 == dict_speaker_points3:
        data = numpy.hstack((mat_pitch, numpy.hstack((mat_f1, mat_f2))))
        print data.shape
        return data, nb_file1, dict_speaker_points1
    else: return None
    
# ---------- visualization Pitch + 2 Formants --------
def visualize_pitch_and_formants(data, nb_cluster, nb_file, dict_speaker_points, legend_title = '', show_pitch=True, show_f1=True, show_f2=True):
    if [show_pitch, show_f1, show_f2].count(True) != 2 and [show_pitch, show_f1, show_f2].count(True) != 3:
         raise ValueError('Must have at least 2 dimensions!')
    
    colors = ['r', 'b', 'g', 'y', 'c', 'm', 'orange', 'navy', 'purple', 'limegreen']
    my_marker = '+'
    
    fig = plt.figure()
    if [show_pitch, show_f1, show_f2].count(True) == 2:
        ax = plt.subplot(111)
    elif [show_pitch, show_f1, show_f2].count(True) == 3:
        ax = plt.subplot(111, projection = '3d')
        ax.set_xlabel('Pitch')
        ax.set_ylabel('Formant1')
        ax.set_zlabel('Formant2')
        
    points = numpy.empty((nb_file, 3, nb_cluster)) # array of all point 2d-arrays
    count = 0
    # plot points
    for speaker in dict_speaker_points:
	# get points in all files of this speaker
        file_number = dict_speaker_points[speaker]
        xx = []
        yy = []
        zz = []
        for i in file_number:
            segment = data[nb_cluster*(i-1): nb_cluster*i, :]	# lines corresponding to each file
            points[i-1] = numpy.transpose(segment)
            xs = points[i-1, 0]	# first line --> pitch
            ys = points[i-1, 1]	# second line --> formant1
            zs = points[i-1, 2]	# third line --> formant2
            xx.extend(xs)	# append all points of this speaker
            yy.extend(ys)
            zz.extend(zs)
        
        if [show_pitch, show_f1, show_f2].count(True) == 3:
            ax.scatter(xx, yy, zz, c=colors[count], marker=my_marker, label=speaker)
        elif [show_f1, show_f2] == [True, True]:
            ax.set_xlabel('Formant1')
            ax.set_ylabel('Formant2')
            ax.scatter(yy, zz, c=colors[count], marker=my_marker, label=speaker)
        elif [show_pitch, show_f1] == [True, True]:
            ax.set_xlabel('Pitch')
            ax.set_ylabel('Formant1')
            ax.scatter(xx, yy, c=colors[count], marker=my_marker, label=speaker)
        else:    
            ax.set_xlabel('Pitch')
            ax.set_ylabel('Formant2')
            ax.scatter(xx, zz, c=colors[count], marker=my_marker, label=speaker)
            
        count = count+1
        print speaker, "\nXX:\n", xx
        print speaker, "\nYY:\n", yy
        print speaker, "\nZZ:\n", zz
        
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
 
     # add legend
    legend = ax.legend(loc='center left', title=legend_title, bbox_to_anchor=(1, 0.5), fontsize='small')
#    legend.get_frame().set_facecolor=('silver')
    
    #fig.savefig('image_output.png', dpi=300, format='png', bbox_extra_artists=(legend,), bbox_inches='tight')
    plt.show()
 
# ========== TEST =======
# file name format: 'Gerra_to_Chirac_1.txt'
nb_cluster = 4

# Imitation by the same person
base_dir = '/media/winE/[TelecomParisTech]/Cours-3A/PIM-imitation/test/Gerra/'
is_same_speaker = True
legend_title = 'Gerra\'s Imitation\n--MFCC'
'''
 # Imitation to the same person
base_dir = '/media/winE/[TelecomParisTech]/Cours-3A/PIM-imitation/test/to_Sarkozy/'
is_same_speaker = False
legend_title = 'Imitation to Sarkozy\n--MFCC'
'''
dir_mfcc = base_dir + 'mfcc/'
dir_pitch = base_dir + 'pitch/'
dir_formant1 = base_dir + 'formant_1/'
dir_formant2 = base_dir + 'formant_2/'
#get_matrix_all_speakers(nb_cluster, dir_pitch, 'pitch')
#get_matrix_all_speakers(nb_cluster, dir_formant1, 'formant')
#get_matrix_all_speakers(nb_cluster, dir_formant2, 'formant')

'''
data, nb_file, dict_speaker_points =  get_matrix_pitch_formant(nb_cluster, dir_pitch, dir_formant1, dir_formant2, is_same_speaker)
# 3D
visualize_pitch_and_formants(data, nb_cluster,nb_file, dict_speaker_points, legend_title)
# projection 2D
visualize_pitch_and_formants(data, nb_cluster,nb_file, dict_speaker_points, legend_title, show_pitch = False)
visualize_pitch_and_formants(data, nb_cluster,nb_file, dict_speaker_points, legend_title, show_f2 = False)
visualize_pitch_and_formants(data, nb_cluster,nb_file, dict_speaker_points, legend_title, show_f1 = False)
'''
#----------Launche MFCC-----------

data, nb_file, dict_speaker_points = get_matrix_all_speakers(nb_cluster, dir_mfcc, 'mfcc', is_same_speaker)
two_dim_matrix = get_reduced_matrix_pca(data, nb_cluster, dir_mfcc)
visualize_mfcc_2D(data, two_dim_matrix, nb_file, dict_speaker_points, legend_title)
