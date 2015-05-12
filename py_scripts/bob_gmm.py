#!/usr/bin/python

import numpy
import bob.learn.misc
import readMatrix

def get_gmm_model (nb_cluster, directory, file_matrix):
# ---parameters---
    max_iter = 200
    converge_threshold = 1e-5 

# ---read MFCC data from Matrix file---
    nb_dim, nb_obsv, matrix = readMatrix.read_matrix(directory, file_matrix)

    nb_dimension = matrix.shape[0] # = 12
    nb_observation = int(nb_obsv)
    data = numpy.transpose(matrix)

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
'''
directory = '/media/winE/[TelecomParisTech]/Cours-3A/PIM-imitation/test/mfcc/'
file_matrix= 'Gerra_to_Chirac_1.txt'
get_gmm_model(4, directory, file_matrix)
'''


