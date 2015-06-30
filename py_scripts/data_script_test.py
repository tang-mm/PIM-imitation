# -*- coding: utf-8 -*-
"""
@author: tangmm
"""
import numpy as np
from os import listdir
import data_reader, data_gmm, data_visualize
#########################################################
# GLOBAL SETTINGS
#########################################################
base_dir = '/media/winE/[TelecomParisTech]/Cours-3A/PIM-imitation/test/'

speaker_dir = base_dir + 'to_Sarkozy/'
speaker = 'Sarkozy'
is_same_imitator = False    # True if one imitator imites several target persons; False otherwise.

# sub-directories
dir_mfcc = speaker_dir + 'mfcc/'
dir_pitch = speaker_dir + 'pitch/'
dir_formant1 = speaker_dir + 'formant_1/'
dir_formant2 = speaker_dir + 'formant_2/'
dir_gmm = speaker_dir + 'gmm/'
dir_likelihood = speaker_dir + 'likelihood/'

n_gaussian = 4      # variant

# set legend title
if is_same_imitator:
    legend_title = speaker + '\'s Imitation' # e.g. 'Gerra's Imitation'
else:
    legend_title = 'Imitation to ' + speaker  # e.g. 'Imitation to Sarkozy'   

##########################################################
#--------I/O Functions--------------
def save_data_to_file(filename, matrix, dict_speaker_files):
    '''
    Save GMM means matrix and the 'Speaker - Line' correspondance to file.
    
    Input:
        matrix: array, shape = ((n_gaussian * n_file), n_dim)
            for MFCC: n_dim = 12
            for Pitch and Formant: n_dim = 3, with 1st colomn = pitch, 2nd & 3rd colomn = formant1 & formant2
        dict_speaker_files: dictionary, (string, list(int))
    '''
    with open(filename, 'wb+') as outfile:
        # save dictionary: dict_speaker_files
        for key, value in dict_speaker_files.items():
            outfile.write(str(key) + '\t' + ','.join(map(str,value)) + '\n')
        # save matrix
        outfile.write('\n')
        np.savetxt(outfile, matrix)


def load_data_from_file(filename):
    '''
    Load GMM means matrix from text file and restore 'Speaker - Line' dictionary.
    
    Return:
        matrix: array, shape = ((n_gaussian * n_file), n_dim)
            for MFCC: n_dim = 12
            for Pitch and Formant: n_dim = 3, with 1st colomn = pitch, 2nd & 3rd colomn = formant1 & formant2
        dict_speaker_files: dictionary, (string, list(int))
    '''
    # load dictionary: dict_speaker_files    
    dict_speaker_files = {}
    with open(filename, 'r') as infile:
        for line in infile:
            if line != '\n':
                elems = line.split('\t')
                speaker = elems[0]
                lines = map(int, elems[1].split(','))
                dict_speaker_files[speaker] = lines
                print speaker, lines
            else:
                break
    n_speaker = len(dict_speaker_files.keys())
    # load matrix
    matrix = np.loadtxt(filename, skiprows = n_speaker)
    print 'matrix: ', matrix.shape
    return matrix, dict_speaker_files
    
#########################################################
#-----------Calculate GMM means of MFCC------------------
#########################################################
data, n_file, dict_speaker_files = data_gmm.get_gmm_mean_all_speakers(n_gaussian, dir_mfcc, 'mfcc', is_same_imitator)

# save to file
filename = dir_gmm + speaker + '_gmm' + str(n_gaussian) + '_mfcc.txt'
save_data_to_file(filename, data, dict_speaker_files)

# visualization
visualize = False #True
if visualize:
    # get matrix for PCA
    two_dim_matrix = data_gmm.get_reduced_mfcc_matrix_pca(data, n_gaussian)
    # visualize
    data_visualize.visualize_mfcc_2D(data, two_dim_matrix, n_file, dict_speaker_files, legend_title + '--MFCC')


#########################################################
#--------Calculate GMM means of Pitch and Formant----------
#########################################################
data, n_file, dict_speaker_files =  data_gmm.get_matrix_pitch_formant(n_gaussian, dir_pitch, dir_formant1, dir_formant2, is_same_imitator)

# save to file
filename = dir_gmm + speaker + '_gmm' + str(n_gaussian) + '_pitch_formant.txt'
save_data_to_file(filename, data, dict_speaker_files)

# visualization
visualize = False # True
if visualize:
    ## 3D
    data_visualize.visualize_pitch_and_formants(data, n_gaussian, n_file, dict_speaker_files, legend_title)
    ## projection 2D
    # proj F1-F2
    data_visualize.visualize_pitch_and_formants(data, n_gaussian, n_file, dict_speaker_files, legend_title, show_pitch = False)
    # proj Pitch - F1
    data_visualize.visualize_pitch_and_formants(data, n_gaussian, n_file, dict_speaker_files, legend_title, show_f2 = False)
    # proj Pitch - F2
    data_visualize.visualize_pitch_and_formants(data, n_gaussian, n_file, dict_speaker_files, legend_title, show_f1 = False)

########################################################
# Likelihood: Imitators compared to Target person
#########################################################
is_same_imitator = False
dir_types = [['mfcc', dir_mfcc], ['pitch', dir_pitch], ['f1', dir_formant1], ['f2', dir_formant2]]
dicts_all = dict()  # key = datatype, value = dict_imitator_likelihood

save_to_file = True

for [datatype, mdir] in dir_types:
    print '=================', datatype.upper(), '=================='
        
    mat_real_all = data_reader.concatenate_all_files(mdir, datatype, speaker)
    gmm_real_all = data_gmm.get_gmm_model(n_gaussian, mat_real_all)
    
    dict_imitator_likelihood = dict()
    
    # calculate likelihood and store in dict
    for file_matrix in sorted(listdir(mdir)):
        # get imitator name
        imitator = file_matrix.split('_')[0] # ex. Gerra_to_Sarkozy_1.txt --> Gerra
        # load original MFCC or Pitch or Formant matrix
        new_mat = data_reader.read_matrix_from_file(mdir, file_matrix, datatype) #(n_obs, 12) for MFCC or (n_obs, 1) for Pitch/Formant  
        n_sample = new_mat.shape[0]
        list_likelihood = [gmm_real_all(new_mat[i, :]) for i in range(n_sample)]
        likelihood = np.sum(list_likelihood) / n_sample
        
        if imitator in dict_imitator_likelihood.keys():
            dict_imitator_likelihood[imitator].append(likelihood)
        else: 
            dict_imitator_likelihood[imitator] = [likelihood]
    
    dicts_all[datatype] = dict_imitator_likelihood
    # save to file
    if save_to_file == True:
        save_to_filename = dir_likelihood + speaker + '_likelihood_' + datatype + '_' + str(n_gaussian) + '.txt'
        save_data_to_file(save_to_filename, np.array([]), dict_imitator_likelihood)

# visualization
visualize = True # True
if visualize == True:
    data_visualize.visualize_likelihood(dicts_all, speaker, n_gaussian)
