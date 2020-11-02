from django.views import View
from django.http import HttpResponse
from django.shortcuts import render



def index(request):
    return render(request, 'samples/index.html')
