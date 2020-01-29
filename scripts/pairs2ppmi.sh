

### RUN EPMI ###
pairs1=($matrixfolder/bins/*);
pairs2=($matrixfolder/tr*)
pairDirs=("${pairs1[@]}" "${pairs2[@]}")
for pairDir in "${pairDirs[@]}" 
do

    # Calculate EPMI matrices for each collection of pairs
    python2 modules/hyperwords/hyperwords/counts2pmi.py --cds 0.75 $pairDir/counts $pairDir/pmi

    ### TRANSFORM EPMI to SPPMI (SHIFTED PPMI), STORE AS PICKLED SPACE (from DISSECT package) ###
    python2 space_creation/epmi2sppmi.py $pairDir/pmi $pairDir/ppmi.sm $k
    rm $pairDir/pmi.npz

done
