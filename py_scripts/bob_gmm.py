#!/usr/bin/python

import numpy
import bob.learn.misc
import data_reader

def get_gmm_model (nb_cluster, directory, file_matrix, data_type):
# ---parameters---
    max_iter = 200
    converge_threshold = 1e-5 

#-- determine matrix type --
    if data_type.lower() == 'mfcc':
    # ---read MFCC data from Matrix file---
        nb_dim, nb_obsv, matrix = data_reader.read_mfcc_matrix(directory, file_matrix)
    
        nb_dimension = matrix.shape[0] # = 12
        nb_observation = int(nb_obsv)
        data = numpy.transpose(matrix)
      
    elif (data_type.lower() == 'pitch' or data_type.lower() == 'formant'):
        data = data_reader.read_pitch_or_formant(directory, file_matrix, data_type)
        data = data[numpy.nonzero(data)] # eliminate non-voiced segment (value = 0)
        nb_observation = data.shape[0]
        nb_dimension = 1
        data =  data[:, None] # convert from 1-D to 2-D
        print data.shape
    else:
        raise ValueError('Error: data type must be \'mfcc\', \'pitch\' or \'formant\'!')

# --- KMeans training ---
    kmeans = bob.learn.misc.KMeansMachine(nb_cluster, nb_dimension)
    kmeansTrainer = bob.learn.misc.KMeansTrainer()
    kmeansTrainer.max_iteration = max_iter
    kmeansTrainer.convergence_threshold = converge_threshold

    kmeansTrainer.train(kmeans, data) # train

    print "KMeans: ", kmeans.means

# --- GMM training ---
    gmm = bob.learn.misc.GMMMachine(nb_cluster, nb_dimension)
    gmm.means = kmeans.means

    gmmTrainer = bob.learn.misc.ML_GMMTrainer(True, True, True) # update means/variances/weights at each iteration
    gmmTrainer.convergence_threshold = converge_threshold
    gmmTrainer.max_iteration = max_iter
    gmmTrainer.train(gmm, data)

    print "GMM means: ", gmm.means
    #print ("GMM variances: ", gmm.variances)

    log_likelihood = gmm(data[0, :])
    print "log_likelihood: ", log_likelihood

    return gmm

#======== test =========

nb_cluster = 8
directory = '/media/winE/[TelecomParisTech]/Cours-3A/PIM-imitation/test/formant_2_Gerra_full/'
file_matrix= 'Gerra_to_Sarkozy_1.txt'
get_gmm_model(nb_cluster, directory, file_matrix, 'formant')



