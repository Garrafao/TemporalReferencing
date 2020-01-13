

### EXTRACT PAIRS ###
# BINS 
for bin in "${bins[@]}"
do
    year1="$(cut -d'-' -f1 <<<"$bin")"
    year2="$(cut -d'-' -f2 <<<"$bin")"
    mkdir -p $matrixfolder/bins/$bin
    python2 corpus_processing/extract_pairs.py $corpusfolder/files $matrixfolder/bins/$bin/pairs $win $year1 $year2 $vocab
done
