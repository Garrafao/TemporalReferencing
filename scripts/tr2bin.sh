

### MAKE BINS FROM TR ###

for ((i=0;i<=(( $num_bins - 1 ));i++)); 
do 
    bin=${bins[$i]}
    ref=${refs[$i]}
    year1="$(cut -d'-' -f1 <<<"$bin")"
    year2="$(cut -d'-' -f2 <<<"$bin")"
    
    mkdir -p $outfolder/$bin
    
    python2 space_creation/tr2bin.py $format $trfile $ref $outfolder/$bin/$filename

done
