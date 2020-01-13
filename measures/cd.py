import sys
sys.path.append('./modules/')

import os
from os.path import basename
from docopt import docopt
from dsm import load_pkl_files
import logging
import time
import codecs
import numpy as np
from scipy import spatial

            
def main():
    """
    Compute cosine distance for target pairs from two vector spaces.
    """

    # Get the arguments
    args = docopt("""Compute cosine distance for target pairs from two vector spaces.

    Usage:
        cd.py [-b] [-o] <spacePrefix1> <spacePrefix2> <outPath> [<testset>]

        <spacePrefix1> = path to pickled space without suffix
        <spacePrefix2> = path to pickled space without suffix
        <testset> = path to file with tab-separated word pairs
        <outPath> = output path for result file

    Options:
        -b, --bot   output both targets in one column
        -o, --out   add nan to output if target is not in vocabulary

     Note:
        Important: spaces must be already aligned (columns in same order)! Default outputs only second target in case of target mismatch; you may want to change this for different purposes.
        
    """)
    
    is_both = args['--bot']
    is_out = args['--out']
    spacePrefix1 = args['<spacePrefix1>']
    spacePrefix2 = args['<spacePrefix2>']
    testset = args['<testset>']
    outPath = args['<outPath>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
    
    # Load spaces
    space1 = load_pkl_files(spacePrefix1)
    space2 = load_pkl_files(spacePrefix2)
    
    if testset!=None:
        # target vectors in first/second column are computed from space1/space2
        with codecs.open(testset, 'r', 'utf-8') as f_in:
            targets = [(line.strip().split('\t')[0],line.strip().split('\t')[1]) for line in f_in]
    else:
        # If no test set is provided, compute values for all targets occurring in both spaces
        target_intersection = set([target.decode('utf-8') for target in space1.get_row2id()]).intersection([target.decode('utf-8') for target in space2.get_row2id()])
        targets = zip(target_intersection,target_intersection)
        
    scores = {}
    # Iterate over rows
    for i, (t1, t2) in enumerate(targets):

        # Get row vector1
        if is_out:
            try:
                row1 = space1.get_row(t1.encode('utf8'))
            except KeyError:
                scores[(t1, t2)] = 'nan'
                continue
        else:        
            row1 = space1.get_row(t1.encode('utf8'))
        # Assume it is scipy sparse matrix, if not, assume numpy matrix
        try:
            row_vector1 = row1.get_mat().toarray()[0].tolist()
        except AttributeError:    
            row_vector1 = row1.get_mat().tolist()[0]
            
        # Get row vector2
        if is_out:
            try:
                row2 = space2.get_row(t2.encode('utf8'))
            except KeyError:
                scores[(t1, t2)] = 'nan'
                continue
        else: 
            row2 = space2.get_row(t2.encode('utf8'))
        try:
            row_vector2 = row2.get_mat().toarray()[0].tolist()
        except AttributeError:    
            row_vector2 = row2.get_mat().tolist()[0]        

        
        # Compute cosine distance of vectors
        distance = spatial.distance.cosine(row_vector1, row_vector2)
        scores[(t1, t2)] = distance
        
        
    with codecs.open(outPath +'.csv', 'w', 'utf-8') as f_out:
        for (t1, t2) in targets:
            if is_both:
                print >> f_out, '\t'.join(('%s,%s' % (t1,t2), str(float(scores[(t1, t2)]))))
            else:           
                if t1==t2:
                    print >> f_out, '\t'.join((t1, str(float(scores[(t1, t2)]))))
                else:
                    print >> f_out, '\t'.join((t2, str(float(scores[(t1, t2)]))))

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    
    

if __name__ == '__main__':
    main()
