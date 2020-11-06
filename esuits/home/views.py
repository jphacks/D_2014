from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django import forms
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from pprint import pprint
from django.db.models import Q


from ..models import CustomUserModel, TagModel, PostModel, ESGroupModel
# Create your views here.


class HomeView(View):
    '''
    ログイン後のトップページ
    ES一覧を表示
    '''

    def get(self, request):
        # ログイン中のユーザ名
        login_username = request.user.username
        # ログイン中のユーザpk
        login_user_id = request.user.id

        # テンプレート
        template = 'esuits/home.html'

        es_group_list = ESGroupModel.objects.filter(author=login_user_id)
        es_group_editing_list = es_group_list.filter(is_editing=True)
        es_group_finished_list = es_group_list.filter(is_editing=False)
        context = {
            'editing': es_group_editing_list,
            'finished': es_group_finished_list,
            'username': login_username,
        }

        return render(request, template, context)

    def post(self, request):
        # ログイン中のユーザ名
        login_username = request.user.username
        # ログイン中のユーザpk
        login_user_id = request.user.id

        # テンプレート
        template = 'esuits/home.html'

        es_group_list = ESGroupModel.objects.filter(author=login_user_id)
        es_group_editing_list = es_group_list.filter(is_editing=True)
        es_group_finished_list = es_group_list.filter(is_editing=False)
        context = {
            'editing': es_group_editing_list,
            'finished': es_group_finished_list,
            'username': login_username,
        }

        return render(request, template, context)
