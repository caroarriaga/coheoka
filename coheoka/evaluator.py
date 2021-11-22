# -*- coding: utf-8 -*-
"""
Evaluator based on transition matrix
"""
from __future__ import print_function, division

from nltk import sent_tokenize
from sklearn import svm
from sklearn.model_selection import train_test_split
from scipy.stats import kendalltau as tau
import numpy as np
# cross_validation
from entity_transition import TransitionMatrix
from ranking import transform_pairwise


class Evaluator(object):
    def __init__(self,
                 corpus,
                 shuffle_times=20,
                 origin_label=1,
                 shuffle_label_func=lambda x, y: -1):
        self._corpus = corpus
        self._origin_matrix = self._label_origin_corpus(origin_label)
        self._shuffled_matrix = self._label_shuffled_corpus(shuffle_times,
                                                            shuffle_label_func)
        self._matrix = np.concatenate((self._origin_matrix,
                                       self._shuffled_matrix))
        self._X, self._y, self._clf, self._fitted_clf = None, None, None, None

    @property
    def corpus(self):
        return self._corpus

    @property
    def matrix(self):
        return self._matrix

    @property
    def X(self):
        if self._X is not None:
            return self._X
        else:
            raise AttributeError(
                'Not generated. Please call `make_data_and_clf` first.')

    @property
    def y(self):
        if self._y is not None:
            return self._y
        else:
            raise AttributeError(
                'Not generated. Please call `make_data_and_clf` first.')

    @property
    def clf(self):
        if self._clf is not None:
            return self._clf
        else:
            raise AttributeError(
                'Not generated. Please call `make_data_and_clf` first.')

    @property
    def fitted_clf(self):
        if self._fitted_clf is not None:
            return self._fitted_clf
        else:
            raise AttributeError('Not generated. Please call `fit` first.')

    def _label_origin_corpus(self, label):
        res = []
        for text in self.corpus:
            res.append((text, label))
        return res

    def _label_shuffled_corpus(self, times, label_func):
        return sum(
            [self._shuffle_text(text, times, label_func)
             for text in self.corpus], [])

    def _shuffle_text(self, text, times, label_func):
        from random import shuffle
        origin_sents = sent_tokenize(text)
        assert len(origin_sents) > 1
        sents = sent_tokenize(text)
        res = []
        for i in range(times):
            shuffle(sents)
            label = label_func(sents, origin_sents)
            res.append((' '.join(sents[:-1]), label))
        return res

    def make_data_and_clf(self, clf=svm.LinearSVC):
        if self._X is None:
            self._X = TransitionMatrix([c for c in self.matrix[:, 0]
                                        ]).tran_matrix.values
            self._y = self.matrix[:, 1].astype(int)
            self._clf = clf
        else:
            pass
        return self

    def predict(self, clf, X):
        return np.dot(X, clf.coef_.ravel())

    def get_ranking_order(self, clf, X):
        return np.argsort(clf.predict(X))

    def evaluate_tau(self, test_size=0.3):
        X, y = transform_pairwise(self.X, self.y)
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size)
        c = self.clf()
        c.fit(X_train, y_train)
        return tau(self.predict(c, X_test), y_test)

    def evaluate_accuracy(self, test_size=0.3):
        X, y = transform_pairwise(self.X, self.y)
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size)
        c = self.clf()
        c.fit(X_train, y_train)
        return c.score(X_test, y_test)

    def fit(self):
        X, y = transform_pairwise(self.X, self.y)
        self._fitted_clf = self.clf().fit(X, y)
        return self

    def evaluate_coherence(self, text):
        x = TransitionMatrix([text]).tran_matrix.values
        return self.predict(self.fitted_clf, x)


def test(*text):
    e = Evaluator(text).make_data_and_clf()
    print([e.evaluate_accuracy() for i in range(5)])
    print([e.evaluate_tau()[0] for i in range(5)])
    t = 'My friend is Bob. He loves playing basketball. And he also is good at tennis.'  # NOQA
    e.fit()
    print(e.evaluate_coherence(t))


if __name__ == '__main__':
    T1 = 'My friend is Bob. He loves playing basketball. And he also is good at tennis.'  # NOQA

    T2 = 'I have a friend called Bob. He loves playing basketball. I also love playing basketball. We play basketball together sometimes.'  # NOQA
    T3 = 'I like apple juice. He also likes it. And he almost drinks apple juice every day.'  # NOQA

    test(*[T1, T2, T3])
