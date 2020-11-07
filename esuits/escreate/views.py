from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from pprint import pprint
from django.db.models import Q

from .forms import CreateESForm, CreatePostForm
from ..models import CustomUserModel, TagModel, PostModel, ESGroupModel
# Create your views here.


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
            extra=1,
        )
        context = {
            'es_form': CreateESForm(),
            # 'post_form': CreatePostForm(),
            'post_formset': PostFormset(form_kwargs={'user': request.user}),
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
            es_file.is_editing = True
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
        post_formset = PostFormset(request.POST, form_kwargs={'user': request.user})

        if post_formset.is_valid():
            print('post_formset')
            print(post_formset.is_valid())
            post_forms = post_formset.save(commit=False)
            for post_form in post_forms:
                post_form.es_group_id = es_group_id
                post_form.save()
            post_formset.save_m2m()
            print('saved post_form')
        else:
            print('failed save post_form')

        return redirect('esuits:es_edit', es_group_id=es_group_id.pk)
