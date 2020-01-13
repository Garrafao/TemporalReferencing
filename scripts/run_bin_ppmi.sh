#!/bin/sh
shopt -s nullglob

# Load parameters
source scripts/params_test.sh
source scripts/prepare_data.sh
source scripts/corpus2vocab.sh

# Extract training pairs
source scripts/corpus2pairs_bins.sh

# Learn vectors
source scripts/pairs2count.sh
source scripts/pairs2ppmi.sh

# Align bins
outfolder=$matrixfolder/align/ppmi
source scripts/ci.sh

# Get results
results=$resultfolder/align/ppmi
filename=ppmi.sm
source scripts/cd_bin.sh
infolder=$matrixfolder/bins
source scripts/knn.sh

