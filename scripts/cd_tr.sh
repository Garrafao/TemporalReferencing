

### MAKE TR RESULTS ###
mkdir -p $results

for ((i=1;i<=(( $num_bins - 1 ));i++)); 
do 
    bin2=${bins[$i]}
    bin1=${bins[$(( $i - 1 ))]}
    ref2=${refs[$i]}
    ref1=${refs[$(( $i - 1 ))]}
    year1="$(cut -d'-' -f1 <<<"$bin1")"
    year2="$(cut -d'-' -f2 <<<"$bin1")"
    year3="$(cut -d'-' -f1 <<<"$bin2")"
    year4="$(cut -d'-' -f2 <<<"$bin2")"
    
    mkdir -p $results/$bin1\_$bin2

    python2 measures/cd.py -b -o $outfolder/$bin1/$filename $outfolder/$bin2/$filename $results/$bin1\_$bin2/cd $targetfolder/targets/double # cosine distance
    
done
