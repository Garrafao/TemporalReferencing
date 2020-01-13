
### MAKE RESULTS ###

for bin in "${bins[@]}" 
do 
    mkdir -p $results/$bin
    python2 measures/knn.py $infolder/$bin/$filename 20 $results/$bin/knn $targetfolder/targets.txt 0 # knn
done
