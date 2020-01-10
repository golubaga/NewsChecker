from django.shortcuts import render

import pickle
import os
import re

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import hstack

from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from collections import Counter

# Create your views here.


class MessageToWordCounterTransform(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        X_transformed = []
        for text in X:
            text = text.lower()
            text = re.sub(r'\d+(?:\.\d*(?:[eE]\d+))?', 'NUMBER', text)
            text = re.sub(r'\W+', ' ', text, flags=re.M)
            word_counts = Counter([word[:-2] for word in text.split() if len(word) > 3 or word == 'NUMBER'])
            X_transformed.append(word_counts)
        return np.array(X_transformed)


class WordCounterToVectorTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, vocabulary_size=1000, vocabulary_=None):
        self.vocabulary_size = vocabulary_size
        if vocabulary_ is not None:
            with open(vocabulary_, 'rb') as f:
                self.vocabulary_ = pickle.load(f)
    def fit(self, X, y=None):
        total_count = Counter()
        for word_count in X:
            for word, count in word_count.items():
                total_count[word] += min(count, 10)
        most_common = total_count.most_common()[:self.vocabulary_size]
        self.most_common_ = most_common
        self.vocabulary_ = {word: index + 1 for index, (word, count) in enumerate(most_common)}
        return self
    def transform(self, X, y=None):
        rows = []
        cols = []
        data = []
        for row, word_count in enumerate(X):
            for word, count in word_count.items():
                rows.append(row)
                cols.append(self.vocabulary_.get(word, 0))
                data.append(count)
        return csr_matrix((data, (rows, cols)), shape=(len(X), self.vocabulary_size + 1))

def predict(text):
    # Loading model
    with open('model.pickle', 'rb') as handle:
        model = pickle.load(handle)
    pipeline = Pipeline([
        ("email_to_wordcount", MessageToWordCounterTransform()),
        ("wordcount_to_vector", WordCounterToVectorTransformer(vocabulary_='vocabulary.pkl')),
    ])

    vector = pipeline.transform([text])
    return model.predict_proba(vector.toarray())[0].tolist()
