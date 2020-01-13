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


def main():
    """
    Convert txt matrix to w2v matrix and save.
    """

    # Get the arguments
    args = docopt('''Convert txt matrix to w2v matrix and save.

    Usage:
        convert_matrix_txt2w2v.py <spacePrefix> <outPath>

        <spacePrefix> = path to npz without suffix
        <outPath> = output path for space
    
    ''')

    spacePrefix = args['<spacePrefix>']
    outPath = args['<outPath>']
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    space_array = np.loadtxt(spacePrefix + '.txt', dtype=object, delimiter=' ', skiprows=0, comments=None, encoding='utf-8')
    targets = space_array[:,0].flatten()
    values = space_array[:,1:].astype(np.float)
    # Create new space
    sparseSpace = Space(DenseMatrix(coo_matrix(values)), list(targets), [])
    
    # Save the Space object in pickle format
    save_pkl_files(sparseSpace, outPath, save_in_one_file=True, save_as_w2v=True)
    
    logging.info("--- %s seconds ---" % (time.time() - start_time))                   

    
if __name__ == '__main__':
    main()
