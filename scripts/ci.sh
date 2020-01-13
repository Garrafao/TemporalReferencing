

### ALIGN MATRICES ###

for ((i=1;i<=(( $num_bins - 1 ));i++)); 
do 
    bin2=${bins[$i]}
    bin1=${bins[$(( $i - 1 ))]}
    year1="$(cut -d'-' -f1 <<<"$bin1")"
    year2="$(cut -d'-' -f2 <<<"$bin1")"
    year3="$(cut -d'-' -f1 <<<"$bin2")"
    year4="$(cut -d'-' -f2 <<<"$bin2")"

    mkdir -p $outfolder/$bin1\_$bin2

    # Align PPMI matrices	
    python2 alignment/ci.py $matrixfolder/bins/$bin1/ppmi.sm $matrixfolder/bins/$bin2/ppmi.sm $outfolder/$bin1\_$bin2/$bin1/ppmi $outfolder/$bin1\_$bin2/$bin2/ppmi # CI alignment

done
