from django.shortcuts import render
from django.views import View

class SinkiSakuseiView(View):
    def get(self,request, *args):
        return render(request, 'esuits/shinkiSakusei.html')