from django.urls import path, include
from . import views
from esuits.samples.newsapi_sample import views as newsapi_view


app_name = 'samples'
urlpatterns = [
    path('', views.index, name='index'),
    path('newsapi/', newsapi_view.newsapi_sample, name='newsapi_sample')
]