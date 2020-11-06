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

from .forms import CreateTagForm
from ..models import TagModel, CustomUserModel
# Create your views here.


class TagCreateView(View):
    '''タグを作成'''

    def get(self, request, *args, **kwargs):
        login_user_id = request.user.id
        template = 'esuits/tag_create.html'
        tags = TagModel.objects.filter(author=login_user_id)
        TagFormset = forms.formset_factory(
            form=CreateTagForm,
            extra=1,
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

        return redirect('esuits:tag_create')
