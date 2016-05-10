# coheoka

Python coherence evaluation tool using Stanford's CoreNLP.

This repository is designed for entity-base coherence.

## Install

You must run a CoreNLP server on your own if you want to run any module in this repository.

You can download Stanford CoreNLP latest version (3.6.0) at [here](http://stanfordnlp.github.io/CoreNLP/download.html) and run a local server (requiring Java 1.8) by this way:

```
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer
```

Then you can find a demo at [`localhost:9000`](http://localhost:9000/), which visualizes StanfordCoreNLP's sophisticated annotation for English documents.

Also, there is an online demo maintained by Stanford at [here](http://corenlp.run/).

Then it is necessary to use a CoreNLP's Python wrapper if you want to communicate with the server, or you can write a wrapper by yourself after reading CoreNLP's documentation. Also, if you are using Windows, make sure you have installed any Python's scientific distribution such as [Anaconda](https://www.continuum.io/downloads) which I strongly recommend. Trust me, you will love it.

This repository does **not** need to install a Python wrapper. The requirements are nltk, numpy, pandas, requests, scipy and scikit-learn.

## Refrence
1. Barzilay, R., & Lapata, M. (2008).
    Modeling local coherence: An entity-based approach.
    Computational Linguistics, 34(1), 1-34.

2. Lapata, M., & Barzilay, R. (2005, July).
    Automatic evaluation of text coherence: Models and representations.
    In IJCAI (Vol. 5, pp. 1085-1090).

## Trivia

### What is the meaning of coheoka?

Coherence + Hyouka (means "evaluation" in Japanese. Kanji: 評価).
