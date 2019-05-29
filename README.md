# TemporalReferencing

Data and code for the experiments in 

- Haim Dubossarsky, Simon Hengchen, Nina Tahmasebi and Dominik Schlechtweg. 2019. Time-Out: Temporal Referencing for Robust Modeling of Lexical Semantic Change. In *Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, Florence, Italy. Association for Computational Linguistics.

If you use this software for academic research, [please cite the paper above](#bibtex) and make sure you give appropriate credit to the below-mentioned software this repository strongly depends on.

The code heavily relies on [DISSECT](http://clic.cimec.unitn.it/composes/toolkit/introduction.html) (modules/composes). For aligning embeddings (SGNS/SVD/RI) we used [VecMap](https://github.com/artetxem/vecmap) (alignment/map_embeddings). For alignment of the PPMI matrices and measuring cosine distance we relied on code from [LSCDetection](https://github.com/Garrafao/LSCDetection). We used [hyperwords](https://bitbucket.org/omerlevy/hyperwords) for training SGNS and PPMI on the extracted word-context pairs.

Usage Note
--------

The scripts should be run directly from the main directory. If you wish to do otherwise, you may have to change the path you add to the path attribute in `sys.path.append('./modules/')` in the scripts. All scripts can be run directly from the command line, e.g.:

	python corpus_processing/extract-pairs.py <windowSize> <corpDir> <outDir> <lowerBound> <upperBound> <testset> <freqset> <minfreq>

We recommend you to run the scripts with the Python Anaconda distribution (Python 2.7.15), only for VecMap Python 3 is needed. You will have to install some additional packages such as: docopt, gensim, i.a. Those that aren't available from the Anaconda installer can be installed via EasyInstall, or by running `pip install -r requirements.txt`. 

### Pipeline

In scripts/run_test.sh you find an example of a full pipeline for the models on a small test corpus. Assuming you are working on a UNIX-based system, first make the script executable with

	chmod 755 scripts/run_test.sh

Then run it with

	bash -e scripts/run_test.sh

Make sure matrices/ is empty each time you run it. You can take a look at the code to understand how it makes use of the different scripts in the repository. It first reads the gzipped test corpus in corpora/test/testcorpus.gz containing many duplicate sentences for the time bins 1920, 1930 and 1940 with each line in the following format:

	year [tab] word1 word2 word3...

It then extracts

1. **regular word-context pairs** for each time bin (for alignment) and
2. **temporarily referenced word-context pairs** for specified target words (target\_year)

with corpus_processing/extract-pairs.py. Then it creates basic matrices for PPMI and SGNS using the scripts under hyperwords/ and aligns the time-binned matrices with the scripts under alignment/. Finally, it extracts cosine distances (displacement) for each pair of adjacent time bins and nearest neighbors for each time bin to results/ using the scripts under measures/. The script measures/displacement.py needs a different input for each model: for the alignment models it takes the file testsets/test/testset-pairs.csv in the following format:

	target1 [tab] target1
	target2 [tab] target2

For Temporal Referencing it takes the files testsets/test/testset-1920-1930-pairs.csv and testsets/test/testset-1930-1940-pairs.csv as input with the following respective formats:

	target1_year1 [tab] target1_year2
	target2_year1 [tab] target2_year2

and

	target1_year2 [tab] target1_year3
	target2_year2 [tab] target2_year3


Data
--------

Under data/ we give a spreadsheet with experimental results on the [Word Sense Change testset](https://zenodo.org/record/495572) and lists of the nearest neighbors for the test words found by the different models when trained on [COHA](https://www.english-corpora.org/coha/) (1920-1970).

BibTex
--------

```
@inproceedings{Dubossarskyetal19,
title = {{Time-Out: Temporal Referencing for Robust Modeling of Lexical Semantic Change}},
author = {Dubossarsky, Haim and Hengchen, Simon and Tahmasebi, Nina and Schlechtweg, Dominik},
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics"
}
```
