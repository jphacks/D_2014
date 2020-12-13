from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django import forms
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout

from ..models import CustomUserModel
# Create your views here.


class SignupView(View):
    '''サインアップ'''

    def get(self, request, *args, **kwargs):
        return render(request, 'esuits/signup.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # ユーザーを登録
        if CustomUserModel.objects.filter(username=username).exists():
            return render(request, 'esuits/signup.html', {'error': 'このユーザー名は既に登録されています'})
        else:
            CustomUserModel.objects.create_user(username, email, password)

        # ログイン
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('esuits:home')
        else:
            return redirect('esuits:login')
