from django.shortcuts import render
from django.views.generic import TemplateView

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

class IndexView(TemplateView):
    template_name = "index.html"

"""
accidents
society
economy
sport
politics
culture
"""

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

article_types = ['Культура', 'Общество', 'Политика', 'Происшествия', 'Спорт', 'Экономика']
article_background_colors = ['primary', 'secondary', 'success', 'danger', 'warning', 'info']

def PredictView(request):
    text = request.POST['accordance_textarea']

    output = list()
    probas = predict(text)
    k = 100 / max(probas)
    probas_scaled = [p * k for p in probas]

    for type, proba, proba_scaled, color in zip(article_types, probas, probas_scaled, article_background_colors):
        output.append({'type': type, 'proba': round(proba * 100, 2), 'color': color, 'proba_scale': proba_scaled})

    return render(request, 'result.html', context={'output': output})

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


class ArticlesView(TemplateView):
    template_name = "articles.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with open('articles.pickle', 'rb') as f:
            links = pickle.load(f)
        context['links'] = links
        return context
