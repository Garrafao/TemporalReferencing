import sys
sys.path.append('./modules/')

import codecs
from collections import defaultdict
import os
from gensim.models.word2vec import PathLineSentences
from docopt import docopt
import logging
import time


def main():
    """
    Make vocabulary from corpus.
    """

    # Get the arguments
    args = docopt("""Make vocabulary from corpus.

    Usage:
        make_vocab.py <corpDir> <outPath> <lowerBound> <upperBound> <minfreq>
        
    Arguments:
       
        <corpDir> = path to zipped corpus directory
        <outPath> = output path for result file
        <lowerBound> = lower bound for time period
        <upperBound> = upper bound for time period
        <minfreq> = minimum frequency threshold

    """)
    
    corpDir = args['<corpDir>']
    outPath = args['<outPath>']        
    lowerBound = int(args['<lowerBound>'])
    upperBound = int(args['<upperBound>'])
    minfreq = float(args['<minfreq>'])

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
             
    freqs = defaultdict(int)      

    data = PathLineSentences(corpDir)
    
    for line in data:
        date, sentence = int(line[:1][0]), line[1:]
        if not lowerBound <= date <= upperBound:
            continue
        for word in sentence:
            freqs[word] = freqs[word] + 1
                       
    with codecs.open(outPath, 'w', 'utf-8') as f_out:
        for word in freqs:
            if freqs[word]>=minfreq:
                f_out.write(word+'\n')
            
    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    

if __name__ == '__main__':
    main()
