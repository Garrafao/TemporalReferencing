import sys
sys.path.append('./modules/')

from docopt import docopt
from dsm import load_pkl_files, save_pkl_files
from composes.semantic_space.space import Space
from composes.matrix.sparse_matrix import SparseMatrix
from composes.matrix.dense_matrix import DenseMatrix
import logging
import time
import codecs

            
def main():
    """
    Convert temporal referencing matrix to regular (binned) matrix.
    """

    # Get the arguments
    args = docopt("""Convert temporal referencing matrix to regular (binned) matrix.

    Usage:
        tr2bin.py (-w | -s) <spacePrefix> <ref> <outPath>

        <spacePrefix> = path to pickled space without suffix
        <ref> = reference string
        <outPath> = output path for result file

    Options:
        -w, --w2v   save in w2v format
        -s, --sps   save in sparse matrix format
        
    """)
    
    is_w2v = args['--w2v']
    is_sps = args['--sps']
    spacePrefix = args['<spacePrefix>']
    ref = args['<ref>']
    outPath = args['<outPath>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
    
    # Load spaces
    space = load_pkl_files(spacePrefix) 
    matrix = space.get_cooccurrence_matrix().get_mat()  
    id2row = space.get_id2row()
    id2column = space.get_id2column()

    ti = [(spl[0],i) for i, w in enumerate(id2row) for spl in [w.split('_')] if len(spl)==1 or (len(spl)==2 and spl[1]==ref)]
    targets, indices = zip(*ti)
    
    new_matrix = matrix[list(indices), :]

    new_space = Space(DenseMatrix(new_matrix), list(targets), id2column)
    
    # Save the Space objects
    if is_w2v:    
        new_space = Space(DenseMatrix(new_matrix), list(targets), id2column)
        save_pkl_files(new_space, outPath, save_in_one_file=True, save_as_w2v=True)
    if is_sps:    
        new_space = Space(SparseMatrix(new_matrix), list(targets), id2column)
        save_pkl_files(new_space, outPath, save_in_one_file=True, save_as_w2v=False)

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    
    

if __name__ == '__main__':
    main()
