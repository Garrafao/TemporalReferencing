import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
import numpy as np
import codecs


def main():
    """
    Make input targets.
    """

    # Get the arguments
    args = docopt("""Make input targets.

    Usage:
        make_targets.py (-t <bound1> <bound2> | -d) <targets> <outpath>
        
    Arguments:
       
        <targets> = path to file with targets
        <outpath> = outpath
        <bound1> = bound1
        <bound2> = bound2

    Options:
        -t, --trf  apply temp ref
        -d, --dou  duplicate targets

    """)
    
    is_trf = args['--trf']
    is_dou = args['--dou']
    targets = args['<targets>']
    outpath = args['<outpath>']
    if is_trf:
        bound1 = args['<bound1>']
        bound2 = args['<bound2>']
        
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Get targets
    with codecs.open(targets, 'r', 'utf8') as f_in:
        targets = [line.strip() for line in f_in]
                        
    with codecs.open(outpath, 'w', 'utf8') as f_out:
        for target in targets:
            if is_trf:
                f_out.write(target+'_'+bound1+'\t'+target+'_'+bound2+'\n')
            if is_dou:
                f_out.write(target+'\t'+target+'\n')


    logging.info("--- %s seconds ---" % (time.time() - start_time))

    
if __name__ == '__main__':
    main()
