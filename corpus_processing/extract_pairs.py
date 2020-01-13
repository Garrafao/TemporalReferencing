import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
import random
import codecs
from gensim.models.word2vec import PathLineSentences


def main():
    """
    Extract training pairs from corpus.
    """

    # Get the arguments
    args = docopt("""Extract training pairs from corpus.

    Usage:
        extract_pairs.py [(-t <targetset> <binfile>)] <corpDir> <outPath> <windowSize> <lowerBound> <upperBound> <vocabset>
        
    Arguments:
       
        <corpDir> = path to corpus directory with zipped files
        <outPath> = path to output file
        <windowSize> = the linear distance of context words to consider in each direction
        <lowerBound> = lower bound for time period
        <upperBound> = upper bound for time period
        <vocabset> = path to file with vocabulary
        <targetset> = path to file with targets
        <binfile> = file with mappings from bins to temporal reference

    Options:
        -t, --trf  apply temp ref

    """)
    
    corpDir = args['<corpDir>']
    outPath = args['<outPath>']
    windowSize = int(args['<windowSize>'])    
    lowerBound = int(args['<lowerBound>'])
    upperBound = int(args['<upperBound>'])
    vocabset = args['<vocabset>']
    is_trf = args['--trf']
    if is_trf:
        targetset = args['<targetset>']
        binfile = args['<binfile>']
        
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Get freqs
    with codecs.open(vocabset, 'r', 'utf8') as f_in:
        vocab = set([line.strip() for line in f_in])

    if is_trf:    
        # Get targets
        with codecs.open(targetset, 'r', 'utf8') as f_in:
            targets = set([line.strip() for line in f_in])
        # Get bins
        with codecs.open(binfile, 'r', 'utf8') as f_in:
            bins = [tuple(line.strip().split('\t')) for line in f_in]
            date2ref = {i:r for (l,u,r) in bins for i in range(int(l),int(u)+1)}
            #print date2ref
            

    # Get pairs
    logging.info("Getting pairs...")
    pairs = []

    data = PathLineSentences(corpDir)
    with codecs.open(outPath, 'w', 'utf8') as f_out:
        for line in data:
            date, sentence = int(line[:1][0]), line[1:]
            if not lowerBound <= date <= upperBound:
                continue
            for i, word in enumerate(sentence):
                lowerWindowSize = max(i-windowSize, 0)
                upperWindowSize = min(i+windowSize, len(sentence))
                window = sentence[lowerWindowSize:i] + sentence[i+1:upperWindowSize+1]
                if word in vocab:
                    if is_trf and word in targets:
                        wstring = word+'_'+date2ref[date]
                    else:
                        wstring = word
                    for contextWord in window:
                        if contextWord in vocab:
                            f_out.write(' '.join((wstring,contextWord))+'\n')
                            

    logging.info("--- %s seconds ---" % (time.time() - start_time))

    
if __name__ == '__main__':
    main()
