from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from .models import CustomUserModel, TagModel, PostModel, ESGroupModel
from django.urls import reverse_lazy, reverse
from django.views import View
# from .forms import HistoryCreateForm, TagCreateForm, UpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

# Create your views here.


class SignupView(View):
    '''サインアップ'''

    def get(self, request, *args, **kwargs):
        return render(request, 'esuits/signup.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # ユーザーを追加
        if CustomUserModel.objects.filter(username=username).exists():
            return render(request, 'esuits/signup.html', {'error': 'このユーザー名  は既に登録されています．'})
        else:
            CustomUserModel.objects.create_user(username, email, password)
            return redirect('index')


class LoginView(View):
    '''ログイン'''

    def get(self, request, *args, **kwargs):
        return render(request, 'esuits/login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('login')


class IndexView(View):
    '''トップページを表示'''
    def get(self, request):
        template_name = 'esuits/index.html'
        return render(request, template_name)


class HomeView(View):
    '''ログイン後のトップページ'''
    def get(self, request):
        login_username = request.user.username
        template = 'esuites/home.html'
        es_group_list = ESGroupModel.objects.filter(author=login_username)
        es_group_editing_list = es_group_list.filter(is_editing=True)
        es_group_finished_list = es_group_list.filter(is_editing=False)
        context = {
            'editing': es_group_editing_list,
            'finished': es_group_finished_list,
        }
    
        return render(request, template, context)
