#!/bin/sh

### PARAMETERS ### 
declare -a corpus=corpora/test/testcorpus.gz # path to gzipped corpus, should not contain any hyphens or underscores
corpusshort=$(basename "${corpus%.*}")
declare -a freqfile=corpora/test/freqs-testcorpus.csv # path to file with frequencies of all words in corpus, create the file with corpus_processing/get_freqs.py
declare -a freqthr=1.0 # minimum frequency threshold below which words will be ignored
declare -a win=5 # window size for all models
declare -a bounds=(1920 1930 1940) # time bins for which a representation will be learned, in equal steps
declare -a step=10 # difference in years between each adjacent pair of bounds
declare -a firstbound=1920 # first time bin
declare -a lastbound=1940 # last time bin
declare -a testset=testsets/test/testset-pairs.csv # testset with targets for alignment models
declare -a trtestsets=(testsets/test/testset-1920-1930-pairs.csv testsets/test/testset-1930-1940-pairs.csv) # testset with targets for temporal referencing models (special format), must contain '-year1-year2-pairs' right in front of file suffix and cannot contain any other hyphens
declare -a dummytestset=testsets/test/dummy_testset.csv # a dummy testset containing senseless strings that do not occur in the corpus (to extract regular pairs)


### EXTRACT PAIRS ###
# BINS 
for bound in "${bounds[@]}"
do
    mkdir --parents matrices/$corpusshort-$bound
    python -u corpus_processing/extract-pairs.py $win $corpus matrices/$corpusshort-$bound $bound $bound $dummytestset $freqfile $freqthr
done

# TEMPORAL REFERENCING
mkdir --parents matrices/$corpusshort\_tr-$firstbound-$lastbound
python -u corpus_processing/extract-pairs.py $win $corpus matrices/$corpusshort\_tr-$firstbound-$lastbound $firstbound $lastbound $testset $freqfile $freqthr


### RUN SGNS, EPMI ###
pairDirs=(matrices/$corpusshort*)
for pairDir in "${pairDirs[@]}" 
do
    # Create counts for word-context pairs
    hyperwords/scripts/pairs2counts.sh $pairDir/pairs > $pairDir/counts
    python hyperwords/hyperwords/counts2vocab.py $pairDir/counts

    # Calculate EPMI matrices for each collection of pairs
    python hyperwords/hyperwords/counts2pmi.py --cds 0.75 $pairDir/counts $pairDir/pmi

    # Create embeddings with SGNS.
    hyperwords/word2vecf/word2vecf -train $pairDir/pairs -pow 0.75 -cvocab $pairDir/counts.contexts.vocab -wvocab $pairDir/counts.words.vocab -dumpcv $pairDir/sgns.contexts -output $pairDir/sgns.words -threads 40 -negative 5 -size 300 -iters 5 > /dev/null 2>&1

    # Convert from text to numpy format and delete text files
    python hyperwords/hyperwords/text2numpy.py $pairDir/sgns.words
    rm $pairDir/sgns.words
    python hyperwords/hyperwords/text2numpy.py $pairDir/sgns.contexts
    rm $pairDir/sgns.contexts

    # Save the embeddings in textual format 
    python hyperwords/hyperwords/sgns2text.py $pairDir/sgns $pairDir/vectors.txt

    # Evaluate on Word Similarity for validation # UNCOMMENT IF NEEDED FOR VALIDATION
    #echo
    #echo "WS353 Results"
    #echo "-------------"
    #
    #python hyperwords/hyperwords/ws_eval.py --neg 5 PPMI $pairDir/pmi hyperwords/testsets/ws/ws353.txt
    #python hyperwords/hyperwords/ws_eval.py SGNS $pairDir/sgns hyperwords/testsets/ws/ws353.txt

done



### CONVERT TXT to W2V FORMAT ###
declare -a sgnsfiles=(matrices/$corpusshort*/vectors.txt)
for sgnsfile in "${sgnsfiles[@]}"
do
    python -u space_creation/convert_matrix_txt2w2v.py "${sgnsfile%.*}" "${sgnsfile%.*}"
    rm $sgnsfile
done



### TRANSFORM EPMI to SPPMI (SHIFTED PPMI), STORE AS PICKLED SPACE (from DISSECT package) ###
declare -a epmifiles=(matrices/$corpusshort*/pmi.npz)
for epmifile in "${epmifiles[@]}"
do
    python -u space_creation/transform_matrix_epmi2sppmi.py "${epmifile%.*}" $(dirname "$epmifile")/ 5
    rm $epmifile
done




### ALIGN MATRICES, MAKE RESULTS ###
# ALIGN SGNS
declare -a outfolder=matrices/mapped
mkdir --parents $outfolder
declare -a resultfolder=results/mapped
mkdir --parents $resultfolder
mkdir --parents $resultfolder/align
mkdir --parents $resultfolder/align/knn
files=(matrices/$corpusshort*/vectors.w2v)

# ALIGN SGNS
for file1 in "${files[@]}"
do
    for file2 in "${files[@]}"
    do
	dirname1=$(basename $(dirname "$file1"))
	dirname2=$(basename $(dirname "$file2"))
	year1="$(cut -d'-' -f2 <<<"$dirname1")"
	year2="$(cut -d'-' -f2 <<<"$dirname2")"
	d=$(( $year2 - $year1 ))
	
	if [[ ! $dirname1 =~ "_tr-" ]] && [[ ! $dirname2 =~ "_tr-" ]] && [ $d == $step ];
	then
	    
	    python3 -u alignment/map_embeddings.py --normalize unit center --init_identical --orthogonal $file2 $file1 $outfolder/target_"${dirname2}"_map_to_"${dirname1}".w2v $outfolder/source_"${dirname2}"_map_to_"${dirname1}".w2v

	    # Make results
	    python2 -u measures/displacement.py -b -o $outfolder/source_"${dirname2}"_map_to_"${dirname1}" $outfolder/target_"${dirname2}"_map_to_"${dirname1}" $resultfolder/align/$(basename "$testset")-$year2-$year1-sgns-align $testset # displacement
	    
	    python2 -u measures/knn.py "${file1%.*}" 20 $resultfolder/align/knn/knn-$corpusshort-$year1-sgns-align $testset 0 # knn

	    if [ $year2 == $lastbound ];
	    then
		python2 -u measures/knn.py "${file2%.*}" 20 $resultfolder/align/knn/knn-$corpusshort-$year2-sgns-align $testset 0 # knn		
	    fi	
	fi	
    done
done

# ALIGN PPMI
files=(matrices/$corpusshort*/ppmi.sm.pkl)
for file1 in "${files[@]}"
do
    for file2 in "${files[@]}"
    do
	dirname1=$(basename $(dirname "$file1"))
	dirname2=$(basename $(dirname "$file2"))
	year1="$(cut -d'-' -f2 <<<"$dirname1")"
	year2="$(cut -d'-' -f2 <<<"$dirname2")"
	d=$(( $year2 - $year1 ))
	
	if [[ ! $dirname1 =~ "_tr-" ]] && [[ ! $dirname2 =~ "_tr-" ]] && [ $d == $step ];
	then
	    
	    # PPMI alignment	
	    python2 -u alignment/count_alignment_intersect.py $outfolder/source_$dirname2\_intsct_$dirname1 $outfolder/target_$dirname2\_intsct_$dirname1 "${file2%.*}" "${file1%.*}" # align PPMI matrices
	    # Make results
	    python2 -u measures/displacement.py -b -o $outfolder/source_$dirname2\_intsct_$dirname1.sm $outfolder/target_$dirname2\_intsct_$dirname1.sm $resultfolder/align/$(basename "$testset")-$year2-$year1-ppmi-align $testset # displacement

	    python2 -u measures/knn.py "${file1%.*}" 20 $resultfolder/align/knn/knn-$corpusshort-$year1-ppmi-align $testset 0 # knn
	    
	    if [ $year2 == $lastbound ];
	    then
		python2 -u measures/knn.py "${file2%.*}" 20 $resultfolder/align/knn/knn-$corpusshort-$year2-ppmi-align $testset 0 # knn		
	    fi
	fi		    
    done
done

### MAKE TR RESULTS ###

declare -a trfiles=(matrices/$corpusshort\_tr-$firstbound-$lastbound/vectors matrices/$corpusshort\_tr-$firstbound-$lastbound/ppmi.sm)
declare -a resultfolder=results/mapped
mkdir --parents $resultfolder/tr
mkdir --parents $resultfolder/tr/knn
for trtestset in "${trtestsets[@]}"
do
    year1="$(cut -d'-' -f2 <<<$(basename "$trtestset"))"
    year2="$(cut -d'-' -f3 <<<$(basename "$trtestset"))"

    for trfile in "${trfiles[@]}"
    do
	
	if [[ $(basename "$trfile") =~ "ppmi" ]];
	then
	    declare -a suffix=ppmi
	else
	    declare -a suffix=sgns
	fi
        
	python2 -u measures/displacement.py -b -o $trfile $trfile $resultfolder/tr/$(basename "$testset")-$year2-$year1-$suffix-tr $trtestset # displacement
	
	python2 -u measures/knn.py $trfile 20 $resultfolder/tr/knn/knn-$corpusshort-$year1-$suffix-tr $trtestset 0 # knn

	if [ $year2 == $lastbound ];
	then
	    python2 -u measures/knn.py $trfile 20 $resultfolder/tr/knn/knn-$corpusshort-$year2-$suffix-tr $trtestset 1 # knn		
	fi
	
    done
done


