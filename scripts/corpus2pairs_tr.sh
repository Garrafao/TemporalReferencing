
# TEMPORAL REFERENCING
mkdir -p $matrixfolder/tr
python2 corpus_processing/extract_pairs.py -t $targetfolder/targets.txt $binfile $corpusfolder/files $matrixfolder/tr/pairs $win $firstbound $lastbound $vocab
