# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from ..models import QuestionModel


class QuestionListView(View):
    '''質問を一覧表示'''
    
    def get(self, request):
        login_user = request.user
        print(type(login_user))
        print(login_user)
        print(login_user.pk)
        login_user_name = login_user.username

        # テンプレート
        template = 'esuits/question_list.html'

        questions = QuestionModel.objects.filter(entry_sheet__author=login_user)
        print(questions)
        context = {
            'username': login_user_name,
            'questions': questions
        }
        return render(request, template, context)
        