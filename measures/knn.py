import sys
sys.path.append('./modules/')

import os
from os.path import basename
from docopt import docopt
from dsm import load_pkl_files
import codecs
import numpy as np
from scipy import spatial
from composes.similarity.cos import CosSimilarity
import logging
import logging.config
import time

            
def main():
    """
    Compute k nearest neighbors for targets.
    """

    # Get the arguments
    args = docopt("""Compute  k nearest neighbors for targets.

    Usage:
        knn.py <spacePrefix1> <k> <outPath> [<testset> <co>]

        <spacePrefix1> = path to pickled space without suffix
        <testset> = path to file with tab-separated word pairs
        <co> = column index for targets
        <k> = parameter k (k nearest neighbors)
        <outPath> = output path for result file

    Note:
        ...
        
    """)
    
    spacePrefix1 = args['<spacePrefix1>']
    testset = args['<testset>']
    co = int(args['<co>'])
    outPath = args['<outPath>']
    k = int(args['<k>'])
    
    logging.config.dictConfig({'version': 1, 'disable_existing_loggers': True,})
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Load spaces
    space1 = load_pkl_files(spacePrefix1)

    if testset!=None:
        with codecs.open(testset, 'r', 'utf8') as f_in:
            targets = [line.strip().split('\t')[co] for line in f_in]
    else:
        # If no test set is provided, compute values for all targets occurring in both spaces
        targets = [target.decode('utf8') for target in space1.get_row2id()]
    
    target2neighbors = {}
    for i,t1 in enumerate(targets):
        
        try:
            neighbors1 = space1.get_neighbours(t1.encode('utf8'), k, CosSimilarity())
            del neighbors1[0]
        except KeyError:
            neighbors1 = [('nan',float('nan'))]
            
        target2neighbors[t1] = neighbors1
               

    with codecs.open(outPath +'.csv', 'w', 'utf-8') as f_out:
        for t1 in targets:
            # Convert cosine similarity to cosine distance, export nearest neighbors
            print >> f_out, t1+'\t'+' '.join([str((n,1-v)) for (n,v) in target2neighbors[t1]])

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
  

if __name__ == '__main__':
    main()
