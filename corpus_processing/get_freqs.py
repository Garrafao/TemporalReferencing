import sys
sys.path.append('./modules/')

import codecs
from collections import defaultdict
import os
from dsm import PathLineSentences_mod
from docopt import docopt
import logging
import time


def main():
    """
    Get frequencies from corpus.
    """

    # Get the arguments
    args = docopt("""Get frequencies from corpus.

    Usage:
        get_freqs.py <corpDir> <outPath> <lowerBound> <upperBound>
        
    Arguments:
       
        <corpDir> = path to zipped corpus directory
        <outPath> = output path for result file
        <lowerBound> = lower bound for time period
        <upperBound> = upper bound for time period

    """)
    
    corpDir = args['<corpDir>']
    outPath = args['<outPath>']        
    lowerBound = int(args['<lowerBound>'])
    upperBound = int(args['<upperBound>'])

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
             
    freqs = defaultdict(int)      

    sentences = PathLineSentences_mod(corpDir, lowerBound=lowerBound, upperBound=upperBound)

    for sentence in sentences:
        for word in sentence:
            freqs[word.lower()] = freqs[word.lower()] + 1
                       
    # Rank the lemmas
    freqs_ranked = sorted(freqs, key=lambda x: -(freqs[x]))

    with codecs.open(outPath + '.csv', 'w', 'utf-8') as f_out:
        for word in freqs_ranked:
            print >> f_out, '\t'.join((word, str(float(freqs[word]))))
            
    logging.info('total number of tokens: %d' % (sentences.corpusSize))
    logging.info('total number of types: %d' % (len(freqs_ranked)))
    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    

if __name__ == '__main__':
    main()
