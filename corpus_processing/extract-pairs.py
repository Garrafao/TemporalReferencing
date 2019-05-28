import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
import re
import numpy as np
import codecs
from dsm import PathLineSentences_mod2


def main():
    """
    Extract training pairs from corpus.
    """

    # Get the arguments
    args = docopt("""Extract training pairs from corpus.

    Usage:
        extract-pairs.py <windowSize> <corpDir> <outDir> <lowerBound> <upperBound> <testset> <freqset> <minfreq>
        
    Arguments:
       
        <corpDir> = path to corpus directory with zipped files
        <outDir> = output dir
        <windowSize> = the linear distance of context words to consider in each direction
        <lowerBound> = lower bound for time period
        <upperBound> = upper bound for time period
        <testset> = path to file with tab-separated word pairs
        <freqset> = path to file with frequency of each word in the corpus
        <minfreq> = min frequency threshold

    """)
    
    corpDir = args['<corpDir>']
    outDir = args['<outDir>']
    windowSize = int(args['<windowSize>'])    
    lowerBound = int(args['<lowerBound>'])
    upperBound = int(args['<upperBound>'])
    testset = args['<testset>']
    freqset = args['<freqset>']
    minfreq = float(args['<minfreq>'])
        
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Get targets
    with codecs.open(testset, 'r', 'utf8') as f_in:
        targets = set([line.strip().split('\t')[0] for line in f_in])

    # Get freqs
    with codecs.open(freqset, 'r', 'utf8') as f_in:
        freqs = {line.strip().split('\t')[0]:float(line.strip().split('\t')[1]) for line in f_in}

    # Get pairs
    logging.info("Getting pairs...")
    pairs = []

    sentences = [s for s in PathLineSentences_mod2(corpDir, lowerBound=lowerBound, upperBound=upperBound)]
    np.random.shuffle(sentences)
    for date, sentence in sentences:
        for i, word in enumerate(sentence):
            word = word.lower()
            lowerWindowSize = max(i-windowSize, 0)
            upperWindowSize = min(i+windowSize, len(sentence))
            window = sentence[lowerWindowSize:i] + sentence[i+1:upperWindowSize+1]
            if freqs[word]>=minfreq and bool(re.match("^[a-zA-Z]+(-[a-zA-Z]+)*$", word)): # exclude strings with special characters
                if word in targets:                
                    wstring = word+'_'+str(date)               
                else:
                    wstring = word          
                for contextWord in window:
                    contextWord = contextWord.lower()
                    if freqs[contextWord]>=minfreq and bool(re.match("^[a-zA-Z]+(-[a-zA-Z]+)*$", contextWord)):
                        pairs.append((wstring,contextWord))

                        
    with codecs.open(outDir+'/'+'pairs', 'w', 'utf8') as f_out:
        for p in pairs:
            f_out.write(' '.join(p)+'\n')

    logging.info("--- %s seconds ---" % (time.time() - start_time))

    
if __name__ == '__main__':
    main()
