
pairs1=($matrixfolder/bins/*);
pairs2=($matrixfolder/tr*)
pairDirs=("${pairs1[@]}" "${pairs2[@]}")
for pairDir in "${pairDirs[@]}" 
do
    # Create counts for word-context pairs
    hyperwords/scripts/pairs2counts.sh $pairDir/pairs > $pairDir/counts
    python2 hyperwords/hyperwords/counts2vocab.py $pairDir/counts
done
