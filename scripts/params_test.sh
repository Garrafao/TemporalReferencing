#!/bin/sh

### PARAMETERS ###
corpusfolder=corpus/test
targetfolder=testsets/test
matrixfolder=matrices/test
resultfolder=results/test
freqthr=1 # minimum frequency threshold below which words will be ignored
win=5 # window size for all models
dim=5 # vector dimensionality
k=5 # number of negative samples
it=5 # number of iterations over data
threads=40 # number of threads you have available on your machine
firstbound=1915 # first time bound
lastbound=1940 # last time bound
binsize=10 # size of bins
