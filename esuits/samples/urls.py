from django.urls import path, include
from . import views
from esuits.samples.newsapi_sample import views as newsapi_view
from esuits.samples.change_color_sample import views as change_color_view


app_name = 'samples'
urlpatterns = [
    path('', views.index, name='index'),
    path('newsapi/', newsapi_view.newsapi_sample, name='newsapi_sample'),
    path('changecolor/', change_color_view.change_color_sample, name="change_color_sample"),
]