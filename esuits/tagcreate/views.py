from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django import forms
from django.urls import reverse_lazy, reverse
from django.views import View

from .forms import CreateTagForm
from ..models import TagModel, CustomUserModel
# Create your views here.


class TagCreateView(View):
    '''タグを作成'''

    def get(self, request, *args, **kwargs):
        login_user_id = request.user.id
        template = 'esuits/tag_create.html'
        tags = TagModel.objects.filter(authors=login_user_id)
        print(tags)
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
        author = CustomUserModel.objects.get(pk=login_user_id)
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
                # タグそのものが存在する場合はそれを取得して，そうでない場合は新規作成
                try:
                    tag = TagModel.objects.get(tag_name=tag_form.tag_name)
                except TagModel.DoesNotExist:
                    tag = TagModel(tag_name=tag_form.tag_name)
                    tag.save()
                    print('saved new tag')
                tag.authors.add(author)
            print('saved post_form')
        else:
            print('failed save post_form')

        return redirect('esuits:tag_create')
