from django.shortcuts import render
from django.views.generic import TemplateView

import pickle
import os
import re

from model.views import predict, WordCounterToVectorTransformer, \
                            MessageToWordCounterTransform

# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"

article_types = ['Культура', 'Общество', 'Политика', 'Происшествия', 'Спорт', 'Экономика']
article_background_colors = ['primary', 'secondary', 'success', 'danger', 'warning', 'info']

def PredictView(request):
    text = request.POST['accordance_textarea']

    if text == '':
        return render(request, 'result.html', context={'empty_request': True})

    output = list()
    probas = predict(text)
    k = 100 / max(probas)
    probas_scaled = [p * k for p in probas]

    for type, proba, proba_scaled, color in zip(article_types, probas, probas_scaled, article_background_colors):
        output.append({'type': type, 'proba': round(proba * 100, 2), 'color': color, 'proba_scale': proba_scaled})

    return render(request, 'result.html', context={'output': output, 'empty_request': False})


class ArticleView(TemplateView):
    template_name = "article.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        with open('articles.pickle', 'rb') as f:
            links = pickle.load(f)

        roi = None
        for link in links:
            if link['pk'] == pk:
                roi = link

        context['article'] = link
        return context


class ArticlesView(TemplateView):
    template_name = "articles.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with open('articles.pickle', 'rb') as f:
            links = pickle.load(f)
        context['links'] = links

        context['total_count'] = len(links)
        counts = {}
        for link in links:
            if not link['class'] in counts.keys():
                counts[link['class']] = 0
            counts[link['class']] += 1

        counts_ = []
        for key, value in counts.items():
            counts_.append({'category_name': key, 'count': value})

        context['category_counts'] = counts_

        return context
