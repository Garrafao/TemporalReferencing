import sys
sys.path.append('./modules/')

import os
import codecs
from os.path import basename
from docopt import docopt
import numpy as np
from dsm import save_pkl_files, load_pkl_files
from composes.semantic_space.space import Space
from composes.matrix.dense_matrix import DenseMatrix
from composes.matrix.sparse_matrix import SparseMatrix
from scipy.sparse import csr_matrix, csc_matrix, coo_matrix
import logging
import time
from scipy import spatial


def main():
    """
    Transform EPMI matrix in npz format to SPPMI space and save as pickle file.
    """

    # Get the arguments
    args = docopt('''Transform EPMI matrix in npz format to SPPMI space and save as pickle file.

    Usage:
        transform_matrix_epmi2sppmi.py <spacePrefix> <outPath> <k>

        <spacePrefix> = path to npz without suffix
        <outPath> = output path for space
        <k> = shifting parameter
    
    ''')

    spacePrefix = args['<spacePrefix>']
    outPath = args['<outPath>']
    k = int(args['<k>'])
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Get npz matrix
    with np.load(spacePrefix + '.npz') as loader:
        matrix = csr_matrix((loader['data'], loader['indices'], loader['indptr']), shape=loader['shape'])


    with open(spacePrefix + '.words.vocab') as f:
        id2row = vocab = [line.strip() for line in f if len(line) > 0]

    with open(spacePrefix + '.contexts.vocab') as f:
        id2column = [line.strip() for line in f if len(line) > 0]
        
    # Apply log weighting
    matrix.data = np.log(matrix.data)

    # Shift values
    matrix.data -= np.log(k)

    # Eliminate negative counts
    matrix.data[matrix.data <= 0] = 0.0

    # Eliminate zero counts
    matrix.eliminate_zeros()
        
    # Create new space
    sparseSpace = Space(SparseMatrix(matrix), id2row, id2column)


    #print sparseSpace.get_cooccurrence_matrix()

    # Save the Space object in pickle format
    save_pkl_files(sparseSpace, outPath + 'ppmi.sm', save_in_one_file=True)
    
    logging.info("--- %s seconds ---" % (time.time() - start_time))                   

    
if __name__ == '__main__':
    main()
