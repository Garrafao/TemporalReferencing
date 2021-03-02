# TemporalReferencing

Data and code for the experiments in 

- Haim Dubossarsky, Simon Hengchen, Nina Tahmasebi and Dominik Schlechtweg. 2019. [Time-Out: Temporal Referencing for Robust Modeling of Lexical Semantic Change](https://www.aclweb.org/anthology/P19-1044/). In *Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, Florence, Italy. Association for Computational Linguistics.

If you use this software for academic research, [please cite the paper above](#bibtex) and make sure you give appropriate credit to the below-mentioned software this repository strongly depends on.

The code heavily relies on [DISSECT](http://clic.cimec.unitn.it/composes/toolkit/introduction.html) (modules/composes). For aligning embeddings (SGNS) we used [VecMap](https://github.com/artetxem/vecmap) (alignment/map_embeddings). For alignment of the PPMI matrices and measuring cosine distance we relied on code from [LSCDetection](https://github.com/Garrafao/LSCDetection). We used [hyperwords](https://bitbucket.org/omerlevy/hyperwords) for training SGNS and PPMI on the extracted word-context pairs.

Usage
--------

The scripts should be run directly from the main directory. If you wish to do otherwise, you may have to change the path you add to the path attribute in `sys.path.append('./modules/')` in the scripts. All scripts can be run directly from the command line, e.g.:

	python2 corpus_processing/extract_pairs.py <corpDir> <outPath> <windowSize> <lowerBound> <upperBound> <vocabset>

We recommend to run the scripts with Python 2.7.15, only for VecMap Python 3 is needed. You will have to install some additional packages such as: docopt, gensim, i.a. Those that aren't available from the Anaconda installer can be installed via EasyInstall, or by running `pip install -r requirements.txt`.


Pipelines
--------

Under `scripts/` we provide full pipelines running the models on a small test corpus. Assuming you are working on a UNIX-based system, first make the scripts executable with

	chmod 755 scripts/*.sh

Then download DISSECT, VecMap and hyperwords with

	bash -e scripts/get_packs.sh

Then run the pipelines with

	bash -e scripts/run_tr_sgns.sh
	bash -e scripts/run_tr_ppmi.sh

	bash -e scripts/run_bin_sgns.sh
	bash -e scripts/run_bin_ppmi.sh

### TR

The Temporal Referencing pipelines for SGNS/PPMI run through the following steps:

1. get vocabulary from corpus (`corpus_processing/make_vocab.py`)
2. extract **temporally referenced word-context pairs** (_word\_year_) for specified target words  (`corpus_processing/extract_pairs.py`)
3. learn one TR matrix for all bins (`modules/hyperwords/`)
4. extract matrix for each bin from TR matrix (`space_creation/tr2bin.py`)
5. extract cosine distances for each pair of adjacent time bins (`measures/cd.py`)
6. extract nearest neighbors for each time bin (`measures/knn.py`)


### Bins

The bin pipelines run through the following steps:

1. get vocabulary from corpus (`corpus_processing/make_vocab.py`)
2. extract **regular word-context pairs** for each time bin (`corpus_processing/extract_pairs.py`)
3. learn matrix for each bin (`modules/hyperwords/`)
4. align matrices for each pair of adjacent time bins (`alignment/`, `modules/vecmap/`)
5. extract cosine distances from aligned matrix pairs (`measures/cd.py`)
6. extract nearest neighbors for each time bin (`measures/knn.py`)


Corpus
--------

Under `corpus/test/files/` we provide a small test corpus contains many duplicate sentences for the time bins 1920, 1930 and 1940 with each line in the following format:

	year [tab] word1 word2 word3...


Data
--------

Under `data/` we give a spreadsheet with experimental results on the [Word Sense Change testset](https://zenodo.org/record/495572) and lists of the nearest neighbors for the test words found by the different models when trained on [COHA](https://www.english-corpora.org/coha/) (1920-1970).

BibTex
--------

```
@inproceedings{Dubossarskyetal19,
	title = {Time-Out: Temporal Referencing for Robust Modeling of Lexical Semantic Change},
	author = {Haim Dubossarsky and Simon Hengchen and Nina Tahmasebi and Dominik Schlechtweg},
	booktitle = {Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics},
	year = {2019},
	address = {Florence, Italy},
	publisher = {Association for Computational Linguistics},
	pages = {457--470}
}
```
