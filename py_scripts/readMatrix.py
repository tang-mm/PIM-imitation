#!/usr/bin/python

import numpy, csv

# read only the first 12 rows in MFCC matrix (C1-C12)
def read_matrix (directory, filename):
    file_path = directory + filename 

    nb_dimension = 0
    nb_observation = 0

    with open(file_path) as f:
        reader = csv.reader(f, delimiter=' ')
        print '----------', filename, '-----------'
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


# read pitch
#def read_pitch (directory, filename):

#-------- test --------
'''
directory = '/media/winE/[TelecomParisTech]/Cours-3A/PIM-imitation/test/mfcc/'
filename = 'Gerra_to_Chirac_1.txt'

read_matrix (directory, filename)
'''


