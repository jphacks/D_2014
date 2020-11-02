from esuits.esuits_utils.newsapi import newsapi
from django.shortcuts import render
from .forms import NewsAPIForm
from django.http.response import JsonResponse


def newsapi_sample(request):
    name = request.GET.get('name','')
    if name:
        news_list = newsapi.get_news(name)
        return JsonResponse({"news":news_list})
    form = NewsAPIForm()
    return render(request,'samples/newsapi_sample.html', {'form':form})