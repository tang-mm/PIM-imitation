# -*- coding: utf-8 -*-
"""
@author: tangmm
"""

import numpy as np
import bob.learn.misc, bob.learn.linear
from os import listdir


def get_gmm_model (n_gaussian, data):
    '''
    Compute the GMM model with the given number of Gaussians. The initial values are determined by K-means machines.
    
    Input:
        n_gaussian: int
        data: array, shape = (n_observation, n_dimension)
    Return:
        GMMMachine: gmm.means.shape = (n_gaussian, n_dimension)
    '''
# ---parameters---
    max_iter = 200
    converge_threshold = 1e-5 

    n_observation, n_dimension = data.shape
    
# --- KMeans training ---
    kmeans = bob.learn.misc.KMeansMachine(n_gaussian, n_dimension)
    kmeansTrainer = bob.learn.misc.KMeansTrainer()
    kmeansTrainer.max_iteration = max_iter
    kmeansTrainer.convergence_threshold = converge_threshold

    kmeansTrainer.train(kmeans, data) # train

    print "KMeans: ", kmeans.means

# --- GMM training ---
    gmm = bob.learn.misc.GMMMachine(n_gaussian, n_dimension)
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


def get_gmm_mean_all_speakers(n_gaussian, directory, datatype, is_same_imitator):
    '''
    Calculate GMM means for all files of/to the same speaker, then generate an overall matrix containing all GMM means
    
    Input:
        n_gaussian: int
        directory: path
        datatype: string, in ['mfcc', 'pitch', 'formant', 'f1', 'f2'], case-insensitive
        is_same_imitator: boolean
            Indicate whether the voice are made by the same imitator (imitating several different target persons), or several imitators (imitating the same target person).
    
    Return:
        matrix: array, if 'mfcc': shape = ((n_gaussians * n_files), 12)
                        else: shape = ((n_gaussians * n_files), 1)
            Overall GMM-means matrix.
        n_file: int
            Total file number
        dict_speaker_files: dictionary.
            Keep indices of lines containing data from a speaker
    '''
    
    datatype = datatype.lower()
    
    if datatype not in ['mfcc', 'pitch', 'formant', 'f1', 'f1']:
        raise ValueError('Error: data type must be \'mfcc\', \'pitch\', \'f1\', \'f2\' or \'formant\'!')


    import data_reader

    data = np.array([])
    n_file = 0
    dict_speaker_files = {}
    
    for file_matrix in sorted(listdir(directory)):   # sort filenames in order to maintain the same reading order
        n_file = n_file + 1
        
        # get speaker name
        if is_same_imitator: # one speaker imitating N persons
            speaker = file_matrix.split('_')[2] # ex. Gerra_to_Sarkozy_1.txt  --> Sarkozy
        else:
            speaker = file_matrix.split('_')[0] # ex. Gerra_to_Sarkozy_1.txt --> Gerra; Sarkozy_1.txt
                 
        # associate files to speaker name in the order of reading
        if speaker in dict_speaker_files:
            if n_file not in dict_speaker_files[speaker]:
                dict_speaker_files[speaker].append(n_file)
        else:
            dict_speaker_files[speaker] = [n_file]
            
        matrix = data_reader.read_matrix_from_file(directory, file_matrix, datatype) # (n_obs, 12) or (n_obs, 1)        
        # calculate GMM for each .wav 
        gmm = get_gmm_model(n_gaussian, matrix) # (n_gaussian, n_dimension)
        # concatenate and form an overall matrix data of size ((n_gaussians * n_files), 12)
        data = np.concatenate((data, gmm.means)) if data.size else gmm.means

    return data, n_file, dict_speaker_files


def get_matrix_pitch_formant(n_gaussian, dir_pitch, dir_formant1, dir_formant2, is_same_imitator):
    '''
    Put GMM mean matrix of pitch and 2 formants together to generate a new matrix in which: 
        1st colomn = pitch, 2nd & 3rd colomn = formant1 & formant2
    
    Input:
        n_gaussian: int
        dir_pitch, dir_formant1, dir_formant2: path of each directory
        is_same_imitator: boolean
            Indicate whether the voice are made by the same imitator (imitating several different target persons), or several imitators (imitating the same target person).
    
    Return:
        data: array, shape = ((n_gaussians * n_files), 3)
        n_file: int
        dict_speaker_files: dictionary, (string, list(int)
    '''
    # pitch
    mat_pitch, n_file1, dict_speaker_files1 = get_gmm_mean_all_speakers(n_gaussian, dir_pitch, 'pitch', is_same_imitator)
    # formant1   
    mat_f1, n_file2, dict_speaker_files2 = get_gmm_mean_all_speakers(n_gaussian, dir_formant1, 'formant', is_same_imitator)
    # formant2
    mat_f2, n_file3, dict_speaker_files3 = get_gmm_mean_all_speakers(n_gaussian, dir_formant2, 'formant', is_same_imitator)
    print 'Pitch:', mat_pitch.shape, 'Formant 1:', mat_f1.shape, 'Formant 2:', mat_f2.shape

    # check if the reading orders are the same    
    if n_file1 == n_file2 == n_file3 and dict_speaker_files1 == dict_speaker_files2 == dict_speaker_files3:
        data = np.hstack((mat_pitch, np.hstack((mat_f1, mat_f2))))
        print data.shape
        return data, n_file1, dict_speaker_files1


def get_reduced_mfcc_matrix_pca(data, n_gaussian):
    '''
    Reduce MFCC matrix dimension with PCA, used for visualization
    Input:
        data: array, shape = ((n_gaussian * n_file), 12)
    Return:
        reduced matrix of shape (12, 2)
    '''
    print "data size:", data.shape
    
    pcaTrainer = bob.learn.linear.PCATrainer()
    [pca_machine, eig_vals] = pcaTrainer.train(data)
    print "PCA: weights shape", pca_machine.weights.shape
    print "PCA: eig_vals\n", eig_vals
    
    # ---------get first two dimensions -----------
    two_dim_matrix = pca_machine.weights[:, [0,1]]  # first two columns with biggest eig_values
    print "two_dim", two_dim_matrix.shape

    return two_dim_matrix