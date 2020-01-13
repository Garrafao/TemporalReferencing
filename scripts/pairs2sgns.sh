
### RUN SGNS ###
pairs1=($matrixfolder/bins/*);
pairs2=($matrixfolder/tr*)
pairDirs=("${pairs1[@]}" "${pairs2[@]}")
for pairDir in "${pairDirs[@]}" 
do
    # Create embeddings with SGNS.
    hyperwords/word2vecf/word2vecf -train $pairDir/pairs -pow 0.75 -cvocab $pairDir/counts.contexts.vocab -wvocab $pairDir/counts.words.vocab -dumpcv $pairDir/sgns.contexts -output $pairDir/sgns.words -threads $threads -negative $k -size $dim -iters $it #> /dev/null 2>&1

    # Convert from text to numpy format and delete text files
    python2 hyperwords/hyperwords/text2numpy.py $pairDir/sgns.words
    rm $pairDir/sgns.words
    python2 hyperwords/hyperwords/text2numpy.py $pairDir/sgns.contexts
    rm $pairDir/sgns.contexts

    # Save the embeddings in textual format 
    python2 hyperwords/hyperwords/sgns2text.py $pairDir/sgns $pairDir/vectors.txt

    ### CONVERT TXT to W2V FORMAT ###
    python2 space_creation/txt2w2v.py $pairDir/vectors $pairDir/vectors
    rm $pairDir/vectors.txt

done
