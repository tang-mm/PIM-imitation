# -*- coding: utf-8 -*-
"""
@author: tangmm
"""

import numpy as np
#from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

 
################################################################
# --------visualization MFCC -----------
def visualize_mfcc_2D(data, n_gaussian, two_dim_matrix, n_file, dict_speaker_files, legend_title):
    '''
    Plot GMM means of MFCC in 2D.
    
    Input:
        data: array, shape = ((n_gaussian * n_file) * 12)
            GMM means matrix of MFCC of all speakers.
        n_gaussian: int
        two_dim_matrix: array, shape = (12, 2)
            Used for dimension reduction.
        n_file: int
        dict_speaker_files: dictionary
            Indicates which speaker is the values in a line correspond to.
        legend_title: string
            Title to show in the figure's legend.
 
    '''

    colors = ['r', 'b', 'g', 'y', 'c', 'm', 'orange', 'navy', 'purple', 'limegreen']
    my_marker = '+'
    
    fig = plt.figure()
    ax = plt.subplot(111) 	# projection = 3d
    
    points = np.empty((n_file, 2, n_gaussian)) # array of all point 2d-arrays
    count = 0
    # plot points
    for speaker in dict_speaker_files:
	# get points in all files of this speaker
        file_number = dict_speaker_files[speaker]
        xx = []
        yy = []
        for i in file_number:
            segment = data[n_gaussian*(i-1): n_gaussian*i, :]	# lines corresponding to each file
            points[i-1] = np.transpose(np.dot(segment, two_dim_matrix))
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
    
    image_name = legend_title + '_MFCC_' + str(n_gaussian) + '.png'
    fig.savefig(image_name, dpi=300, format='png', bbox_extra_artists=(legend,), bbox_inches='tight')
    plt.show()

  
# ---------- visualization Pitch + 2 Formants --------
def visualize_pitch_and_formants(data, n_gaussian, n_file, dict_speaker_files, legend_title = '', show_pitch=True, show_f1=True, show_f2=True):
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
        
    points = np.empty((n_file, 3, n_gaussian)) # array of all point 2d-arrays
    count = 0
    # plot points
    for speaker in dict_speaker_files:
	# get points in all files of this speaker
        file_number = dict_speaker_files[speaker]
        xx = []
        yy = []
        zz = []
        for i in file_number:
            segment = data[n_gaussian*(i-1): n_gaussian*i, :]	# lines corresponding to each file
            points[i-1] = np.transpose(segment)
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
            image_name = legend_title + '_f1_f2_' + str(n_gaussian) + '.png'
        elif [show_pitch, show_f1] == [True, True]:
            ax.set_xlabel('Pitch')
            ax.set_ylabel('Formant1')
            ax.scatter(xx, yy, c=colors[count], marker=my_marker, label=speaker)
            image_name = legend_title + '_pitch_f1_' + str(n_gaussian) + '.png'
        else:    
            ax.set_xlabel('Pitch')
            ax.set_ylabel('Formant2')
            ax.scatter(xx, zz, c=colors[count], marker=my_marker, label=speaker)
            image_name = legend_title + '_pitch_f2_' + str(n_gaussian) + '.png'
            
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
    
    if [show_pitch, show_f1, show_f2].count(True) != 3:
        fig.savefig(image_name, dpi=300, format='png', bbox_extra_artists=(legend,), bbox_inches='tight')
    plt.show()
 

#-------------------------------------------------------------
def visualize_likelihood(dicts_all, target_speaker, n_gaussian):
    colors = ['r', 'b', 'g', 'y', 'c', 'm', 'orange', 'navy', 'purple', 'limegreen']
    my_marker = 'x'
    mfontsize = 'small'
    
    n_plot = len(dicts_all.keys())  # = 4
    #fig, axes = plt.subplots(nrows=n_plot, ncols=1)
    fig = plt.figure()
    
    for idx in range(n_plot):
        datatype = dicts_all.keys()[idx]
        dict_imitator_likelihood = dicts_all.values()[idx]
    
        ax = fig.add_subplot(n_plot, 1, idx+1)
        i = 0
        for key, value in sorted(dict_imitator_likelihood.items()):
            plt.scatter(value, np.zeros_like(value)+(0.1*i), c=colors[i], marker=my_marker)   
            i += 1
        
        #plt.xlabel('Log-Likelihood')
        #plt.ylabel('Speaker')
        plt.title('Log-Likelihood: ' + datatype.upper(), fontdict={'fontsize':mfontsize})
        plt.xticks(fontsize=mfontsize)
        plt.yticks(0.1*np.arange(i), sorted(dict_imitator_likelihood.keys()), fontsize=mfontsize)
    
    plt.subplots_adjust(hspace=0.5)
    fig.suptitle('Imitation to '+ target_speaker.title() + ' (n = ' + str(n_gaussian) + ' )', fontsize='medium')
    
    image_name = target_speaker + '_likelihood_' + str(n_gaussian) + '.png'
    fig.savefig(image_name, dpi=300, format='png') # , bbox_inches='tight')
    plt.show()
    