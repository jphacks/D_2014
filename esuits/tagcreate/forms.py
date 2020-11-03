from django import forms
from ..models import TagModel


class CreateTagForm(forms.ModelForm):
    '''タグ作成のためのフォーム'''
    class Meta:
        model = TagModel
        fields = ('tag_name',)
