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

wget https://bitbucket.org/omerlevy/hyperwords/get/f5a01ea3e44c.zip
unzip f5a01ea3e44c.zip
rm f5a01ea3e44c.zip
mv omerlevy-hyperwords-f5a01ea3e44c hyperwords

cd hyperwords
chmod 755 *.sh
chmod 755 scripts/*.sh

mkdir word2vecf
wget https://bitbucket.org/yoavgo/word2vecf/get/1b94252a58d4.zip
unzip 1b94252a58d4.zip
rm 1b94252a58d4.zip
mv yoavgo-word2vecf-1b94252a58d4/*.c word2vecf/.
mv yoavgo-word2vecf-1b94252a58d4/*.h word2vecf/.
mv yoavgo-word2vecf-1b94252a58d4/makefile word2vecf/.
rm -r yoavgo-word2vecf-1b94252a58d4
make -C word2vecf word2vecf
