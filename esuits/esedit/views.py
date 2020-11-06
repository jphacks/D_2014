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
from django.http.response import JsonResponse

from .forms import AnswerQuestionFormSet, AnswerQuestionForm
from ..models import CustomUserModel, TagModel, PostModel, ESGroupModel
from ..esuits_utils.newsapi import newsapi
from ..esuits_utils.wordcloudapi.get_wordcloud import get_wordcloud
# Create your views here.


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
        es_info = ESGroupModel.objects.get(pk=es_group_id)
        company_url = es_info.company_url

        wordcloud_path = get_wordcloud(company_url)
        company_info = {"wordcloud_path":wordcloud_path[1:]}
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

                # ニュース関連
                news_list = newsapi.get_news(es_info.company)

                # 企業の情報　(ワードクラウドなど)
                company_info = self._get_company_info(request, es_group_id)

                context = {
                    'message': 'OK',
                    'es_info': es_info,
                    'formset_management_form': formset.management_form,
                    'zipped_posts_info': zip(post_set, formset, related_posts_list),
                    'news_list': news_list,
                    'company_info': company_info,
                    'num_related_posts': len(related_posts_list)
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
                    return redirect('esuits:home')

                # 関連したポスト一覧
                related_posts_list = self._get_related_posts_list(request, es_group_id)

                # ニュース関連
                news_list = newsapi.get_news(es_info.company)

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

def get_related_post(request):
    pk = int(request.GET.get('pk',''))
    es = PostModel.objects.get(pk=pk)
    print(es.question,es.answer,sep='¥n')
    return JsonResponse({'question':es.question, 'answer':es.answer})

def get_wordcloud_path(request):
    es_group_id = int(request.GET.get('es_group_id',''))

    return JsonResponse({'image_path':'ここに画像のパスを入れる'})