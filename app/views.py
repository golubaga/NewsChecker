rom django.shortcuts import render
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

    output = list()
    probas = predict(text)
    k = 100 / max(probas)
    probas_scaled = [p * k for p in probas]

    for type, proba, proba_scaled, color in zip(article_types, probas, probas_scaled, article_background_colors):
        output.append({'type': type, 'proba': round(proba * 100, 2), 'color': color, 'proba_scale': proba_scaled})

    return render(request, 'result.html', context={'output': output})

class ArticlesView(TemplateView):
    template_name = "articles.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with open('articles.pickle', 'rb') as f:
            links = pickle.load(f)
        context['links'] = links
        return context
