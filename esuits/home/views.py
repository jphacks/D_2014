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

        # どのESのis_editingを変更するか
        target_es_id = request.POST['target_es']

        # is_editingの値を反転 (編集中 -> 提出済, 提出済 -> 編集中)
        target_es = ESGroupModel.objects.get(pk=target_es_id)
        target_es.is_editing = not target_es.is_editing
        target_es.save()

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
