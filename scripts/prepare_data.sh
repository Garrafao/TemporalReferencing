mkdir -p $matrixfolder
mkdir -p $targetfolder/targets
vocab=$corpusfolder/vocab
bins=()
i=$firstbound
binfile=$corpusfolder/bins
rm -f $binfile
refs=()

while [ $i -le $lastbound ];
do
    a=$i
    b=$(( $i + $(( $binsize - 1)) ))
    if [ $b -ge $lastbound ];
    then
	b=$lastbound	
    fi	
    bins+=( $(echo -e "$a-$b") )
    i=$(( $b + 1 ))
done

# Export bins and temporal references
num_bins=${#bins[@]}
for bin in "${bins[@]}"
do
    year1="$(cut -d'-' -f1 <<<"$bin")"
    year2="$(cut -d'-' -f2 <<<"$bin")"
    ref=$year1
    refs+=( "$ref" )
    echo -e "$year1\t$year2\t$ref" >> $binfile
done
num_refs=${#refs[@]}

### MAKE TARGETS ###

python2 corpus_processing/make_targets.py -d $targetfolder/targets.txt $targetfolder/targets/double

