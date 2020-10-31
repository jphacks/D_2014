from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from .models import CustomUserModel, TagModel, PostModel, ESGroupModel
from django.urls import reverse_lazy, reverse
from django.views import View
from .forms import CreateESForm, CreatePostForm
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

        # ログイン
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')

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
            return redirect('home')
        else:
            return redirect('login')


class IndexView(View):
    '''トップページを表示'''
    def get(self, request):
        template_name = 'esuits/index.html'
        return render(request, template_name)


class HomeView(View):
    '''
    ログイン後のトップページ
    ES一覧を表示
    '''

    def get(self, request):
        # login_username = request.user.username
        login_user_id = request.user.id
        # print(login_user_id)
        template = 'esuits/home.html'
        es_group_list = ESGroupModel.objects.filter(author=login_user_id)
        es_group_editing_list = es_group_list.filter(is_editing=True)
        es_group_finished_list = es_group_list.filter(is_editing=False)
        context = {
            'editing': es_group_editing_list,
            'finished': es_group_finished_list,
        }
        return render(request, template, context)


class ESCreateView(View):
    '''ポストの質問を作成'''

    def get(self, request, *args, **kwargs):
        login_user_id = request.user.id
        template = 'esuits/es_create.html'
        tags = TagModel.objects.filter(author=login_user_id)
        num_tags = len(tags)

        context = {
            'es_form': CreateESForm(),
            'post_form': CreatePostForm(),
            'tags': tags,
            'num_tags': num_tags,
            'user_id': login_user_id,
        }
        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        login_user_id = request.user.id
        request_copy = request.POST.copy()
        # authorを指定
        request_copy['author'] = login_user_id

        # es情報を取得(必要なし)
        # company = request_copy['company']
        # event_type = request_copy['event_type']
        # author = login_user_id
        # created_date = request_copy['created_date']

        # 先にESフォームからの情報をデータベースに格納
        # es_form = CreateESForm(request_copy, prefix='es')
        es_form = CreateESForm(request_copy)
        print(request_copy)
        print('----------------------')
        print(es_form)
        if es_form.is_valid():
            # form.save()では，作成されたレコードが返ってくる．作成されたレコードのpkを取得
            es_group_id = es_form.save().pk
            print('saved es_form')
        else:
            print('failed save es_form')

        # postフォームをデータベースに格納

        # 回答の文字数を取得
        request_copy['char_num'] = len(request.POST['answer'])
        request_copy['es_group_id'] = es_group_id

        post_form = CreatePostForm(request_copy)
        if post_form.is_valid():
            post_form.save()
            print('saved post_form')
        else:
            print('failed save post_form')

        return redirect('home')
     
