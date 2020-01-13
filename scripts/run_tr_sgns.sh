#!/bin/sh
shopt -s nullglob

# Load parameters
source scripts/params_test.sh
source scripts/prepare_data.sh
source scripts/corpus2vocab.sh

# Extract training pairs
source scripts/corpus2pairs_tr.sh

# Learn vectors
source scripts/pairs2count.sh
source scripts/pairs2sgns.sh

# TR
trfile=$matrixfolder/tr/vectors
outfolder=$matrixfolder/tr/bins/sgns
filename=vectors
format="-w"
source scripts/tr2bin.sh

# Get results
results=$resultfolder/tr/sgns
source scripts/cd_tr.sh
infolder=$outfolder
source scripts/knn.sh
