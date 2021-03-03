#!/bin/sh
cd modules/

wget https://github.com/artetxem/vecmap/archive/master.zip
unzip master.zip
rm master.zip
mv vecmap-master vecmap

wget https://github.com/composes-toolkit/dissect/archive/master.zip
unzip master.zip
rm master.zip
mv dissect-master/src/composes composes
rm -r dissect-master

wget https://github.com/BIU-NLP/hyperwords/archive/master.zip
unzip master.zip
rm master.zip
mv hyperwords-master hyperwords

cd hyperwords
chmod 755 *.sh
chmod 755 scripts/*.sh


wget https://github.com/BIU-NLP/word2vecf/archive/master.zip
unzip master.zip
rm master.zip
mv word2vecf-master word2vecf
make -C word2vecf word2vecf
