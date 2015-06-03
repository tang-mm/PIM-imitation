#!/usr/bin/python

import numpy, csv

# read only the first 12 rows in MFCC matrix (C1-C12)
def read_mfcc_matrix (directory, filename):
    file_path = directory + filename 

    nb_dimension = 0
    nb_observation = 0
    
    with open(file_path) as f:
        reader = csv.reader(f, delimiter=' ')
        print '---------- MFCC: ', filename, '-----------'
        for row in reader:
            if reader.line_num == 3:# line_num begins at 1
                nb_observation = int(row[2])  # get number of columns in matrix
            if reader.line_num == 4:
                nb_dimension = int(row[1]) # get number of rows in matrix
                break

        # read only C1-C12
        data = numpy.loadtxt(f, dtype='float64', delimiter=" ")
        print data.shape
        matrix = data[0:12, :]  # keep C1-C12
        print matrix.shape
    return nb_dimension, nb_observation, matrix


# read 
def read_pitch_or_formant (directory, filename, datatype):
    file_path = directory + filename
        
    with open(file_path) as f:
        reader = csv.reader(f, delimiter=' ')
        print '----------', datatype, ':', filename, '-----------'
        for row in reader:
            print reader.line_num, row
            if reader.line_num == 3:# line_num begins at 1
                nb_observation = int(row[2])  # get number of columns in matrix
            if reader.line_num == 4:
                break
        # only 1 line
        data = numpy.loadtxt(f, dtype='float64', delimiter=" ")
    return data
        
# read 2 formants and return a 2-D array
def read_formant (dir_formant1, dir_formant2, filename):        
    file_path1 = dir_formant1 + filename
    file_path2 = dir_formant2 + filename
    
    # formant F1
    with open(file_path1) as f:
        reader = csv.reader(f, delimiter=' ')
        print '----------', filename, '-----------'
        for row in reader:
            print reader.line_num, row
            if reader.line_num == 3:# line_num begins at 1
                nb_observation = int(row[2])  # get number of columns in matrix
            if reader.line_num == 4:
                break
        # only 1 line
        data1 = numpy.loadtxt(f, dtype='float64', delimiter=" ")
        data1 = data1[:, None]
        print data1.shape
        
    # formant F2
    with open(file_path2) as f:
        reader = csv.reader(f, delimiter=' ')
        print '----------', filename, '-----------'
        for row in reader:
            print reader.line_num, row
            if reader.line_num == 3:# line_num begins at 1
                nb_observation = int(row[2])  # get number of columns in matrix
            if reader.line_num == 4:
                break
        # only 1 line
        data2 = numpy.loadtxt(f, dtype='float64', delimiter=" ")
        data2 = data2[:, None]
        print data2.shape
        
    # form a matrix of 2 colomns, each containing a formant        
    data = numpy.hstack((data1, data2)) # combine by colomn
    print "formant: ", data.shape
    return data
    
#-------- test --------
'''
directory1 = '/media/winE/[TelecomParisTech]/Cours-3A/PIM-imitation/test/formant_1_Gerra_full/'
directory2 = '/media/winE/[TelecomParisTech]/Cours-3A/PIM-imitation/test/formant_2_Gerra_full/'
filename = 'Gerra_to_Chirac_1.txt'

read_formant (directory1, directory2, filename)
'''