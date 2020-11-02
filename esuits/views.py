from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django import forms
from django.urls import reverse_lazy, reverse
from django.views import View
from .forms import CreateESForm, CreatePostForm, AnswerQuestionFormSet
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from pprint import pprint
from django.db.models import Q

from .forms import CreateESForm, CreatePostForm, CreateTagForm
from .models import CustomUserModel, TagModel, PostModel, ESGroupModel
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
            return redirect('esuits:home')
        else:
            return redirect('esuits:login')


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
        login_username = request.user.username
        print(login_username)
        login_user_id = request.user.id
        # print(login_user_id)
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


class ESCreateView(View):
    '''ポストの質問を作成'''

    def get(self, request, *args, **kwargs):
        login_user_id = request.user.id
        template = 'esuits/es_create.html'
        tags = TagModel.objects.filter(author=login_user_id)
        num_tags = len(tags)
        # ポストフォームはformsetを使用
        PostFormset = forms.formset_factory(
            # PostModel,
            form=CreatePostForm,
            extra=2,
        )
        context = {
            'es_form': CreateESForm(),
            # 'post_form': CreatePostForm(),
            'post_formset': PostFormset(),
            'tags': tags,
            'num_tags': num_tags,
            'user_id': login_user_id,
        }
        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        login_user_id = request.user.id
        # es情報を取得(必要なし)
        # company = request_copy['company']
        # event_type = request_copy['event_type']
        # author = login_user_id
        # created_date = request_copy['created_date']

        # 先にESフォームからの情報をデータベースに格納
        # es_form = CreateESForm(request_copy, prefix='es')
        es_form = CreateESForm(request.POST)
        print(request.POST)
        print('----------------------')
        print(es_form)
        if es_form.is_valid():
            # form.save()では，作成されたレコードが返ってくる．作成されたレコードのpkを取得
            es_file = es_form.save(commit=False)
            es_file.author = CustomUserModel.objects.get(pk=login_user_id)
            es_group_id = es_form.save()
            print('saved es_form')
        else:
            print('failed save es_form')

        # postフォームをデータベースに格納

        post_num = int(request.POST['form-TOTAL_FORMS'])
        # 値を変更する
        # 各ポストのes group idを更新
        # for post_num in range(post_num):
        #     post_name = 'form-' + str(post_num) + '-'
        #     es_group_id_key = post_name + 'es_group_id'
        #     request_copy[es_group_id_key] = es_group_id
        # print(request_copy)

        # 回答の文字数を取得
        # request_copy['char_num'] = len(request.POST['answer'])
        # request_copy['es_group_id'] = es_group_id

        # post_form = CreatePostForm(request_copy)

        PostFormset = forms.modelformset_factory(
            model=PostModel,
            form=CreatePostForm,
            extra=post_num,
        )
        post_formset = PostFormset(request.POST)
        if post_formset.is_valid():
            print('post_formset')
            print(post_formset.is_valid())
            post_forms = post_formset.save(commit=False)
            for post_form in post_forms:
                post_form.es_group_id = es_group_id
                post_form.save()
            print('saved post_form')
        else:
            print('failed save post_form')

        return redirect('esuits:home')


class EsEditView(View):
    '''
    ESの質問に回答するページ
    '''

    # 過去に投稿したポストのうち関連するものを取得
    def _get_related_posts_list(self, request, es_group_id):
        post_set = PostModel.objects.filter(es_group_id=es_group_id)
        all_posts_by_login_user = PostModel.objects.filter(es_group_id__author=request.user)

        related_posts_list = [
            all_posts_by_login_user
            .filter(tags__in=post.tags.all())
            .exclude(pk=post.pk)
            for post in post_set
        ]
        return related_posts_list

    # 関連するニュースの取得 (いまはダミー)
    def _get_news_list(self, request, es_group_id):
        news_list = [
            {'title': 'ダミーニュース1', 'url': 'https://news.yahoo.co.jp/pickup/6375312'},
            {'title': 'ダミーニュース2', 'url': 'https://news.yahoo.co.jp/pickup/6375301'},
        ]
        return news_list

    # 企業の情報を取得 (今は空)
    def _get_company_info(self, request, es_group_id):
        company_info = {}
        return company_info

    def get(self, request, es_group_id):
        template_name = 'esuits/es_edit.html'

        if ESGroupModel.objects.filter(pk=es_group_id).exists():
            # ESの存在を確認
            es_info = ESGroupModel.objects.get(pk=es_group_id)
            print('es_info.author.pk: ' + str(es_info.author.pk))
            print('request.user.pk: ' + str(request.user.pk))

            if (es_info.author == request.user):
                # 指定されたESが存在し，それが自分のESの場合
                post_set = PostModel.objects.filter(es_group_id=es_group_id)
                formset = AnswerQuestionFormSet(instance=es_info)

                # 関連したポスト一覧
                related_posts_list = self._get_related_posts_list(request, es_group_id)

                # ニュース関連 (今はダミー)
                news_list = self._get_news_list(request, es_group_id)

                # 企業の情報　(ワードクラウドなど)
                company_info = self._get_company_info(request, es_group_id)

                context = {
                    'message': 'OK',
                    'es_info': es_info,
                    'formset_management_form': formset.management_form,
                    'zipped_posts_info': zip(post_set, formset, related_posts_list),
                    'news_list': news_list,
                    'company_info': company_info,
                }
                return render(request, template_name, context)
            else:
                # 指定されたESが存在するが，それが違う人のESの場合
                context = {
                    'message': '違う人のESなので表示できません',
                    'es_info': {},
                    'zipped_posts_info': (),
                }
                return render(request, template_name, context)
        else:
            # 指定されたESが存在しない場合
            context = {
                'message': '指定されたESは存在しません',
                'es_info': {},
                'zipped_posts_info': (),
            }
            return render(request, template_name, context)

    def post(self, request, es_group_id):
        # TODO: 質問に対する答えを更新してDBに格納する処理を書く
        template_name = 'esuits/es_edit.html'

        if ESGroupModel.objects.filter(pk=es_group_id).exists():
            # ESの存在を確認
            es_info = ESGroupModel.objects.get(pk=es_group_id)
            print('es_info.author.pk: ' + str(es_info.author.pk))
            print('request.user.pk: ' + str(request.user.pk))

            if (es_info.author == request.user):
                # 指定されたESが存在し，それが自分のESの場合
                post_set = PostModel.objects.filter(es_group_id=es_group_id)
                formset = AnswerQuestionFormSet(data=request.POST, instance=es_info)

                if formset.is_valid():
                    formset.save()

                # 関連したポスト一覧
                related_posts_list = self._get_related_posts_list(request, es_group_id)

                # ニュース関連
                news_list = self._get_news_list(request, es_group_id)

                # 企業の情報　(ワードクラウドなど)
                company_info = self._get_company_info(request, es_group_id)

                context = {
                    'message': 'OK',
                    'es_info': es_info,
                    'formset_management_form': formset.management_form,
                    'zipped_posts_info': zip(post_set, formset, related_posts_list),
                    'news_list': news_list,
                    'company_info': company_info,
                }
                return render(request, template_name, context)
            else:
                # 指定されたESが存在するが，それが違う人のESの場合
                context = {
                    'message': '違う人のESなので表示できません',
                    'es_info': {},
                    'zipped_posts_info': (),
                }
                return render(request, template_name, context)
        else:
            # 指定されたESが存在しない場合
            context = {
                'message': '指定されたESは存在しません',
                'es_info': {},
                'zipped_posts_info': (),
            }
            return render(request, template_name, context)


class TagCreateView(View):
    '''タグを作成'''

    def get(self, request, *args, **kwargs):
        login_user_id = request.user.id
        template = 'esuits/tag_create.html'
        tags = TagModel.objects.filter(author=login_user_id)
        TagFormset = forms.formset_factory(
            # PostModel,
            form=CreateTagForm,
            extra=2,
        )
        context = {
            'tag_formset': TagFormset,
            'tags': tags,
            'user_id': login_user_id,
        }
        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        login_user_id = request.user.id
        post_num = int(request.POST['form-TOTAL_FORMS'])
        TagFormset = forms.modelformset_factory(
            model=TagModel,
            form=CreateTagForm,
            extra=post_num,
        )
        tag_formset = TagFormset(request.POST)

        if tag_formset.is_valid():
            tag_forms = tag_formset.save(commit=False)
            for tag_form in tag_forms:
                tag_form.author = CustomUserModel.objects.get(pk=login_user_id)
                tag_form.save()
            print('saved post_form')
        else:
            print('failed save post_form')

        return redirect('esuits:home')
