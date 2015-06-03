File to execute: 

- MFCC matrix files:
dimension (37 * nb_observations). C0 is related to energy; delta and delta-delta are calculated for C1-C12, thus forming 12*3+1=37 lines.

- C1 to C12 are extracted to train GMM machine, get GMM model.
(?? train with 37 and then extract, OR, extract and train?)

- 
===== Python ===================

*** readMatrix.py
- Open text files containing MFCC matrix and return a 2D numpy array (matrix).
- Matrix shape: (nb_cluster * 12).


*** bob_gmm.py
- Call readMatrix function, initiate a GMM machine and train with the MFCC data (c1-c12). Return the trained GMM model.
- GMM means matrix shape: (nb_cluster * 12).


*** bob_pca.py
- concatenate GMM means from all files of the same imitators imitating different speakers, forming a matrix of shape ( 12 * (nb_cluster*nb_file)).
- train PCA machine with the matrix obtained.
- get first tow columns : two_dim_matrix (2 * 12), which correspond to the two dimensions with biggest eigen values (already sorted).
- multiply: two_dim_matrix * GMM_means_of_one_file ==> 2 * nb_cluster
- plot the points in 2D figure.
