from django import forms
from ..models import ESGroupModel, PostModel, TagModel


class CreateESForm(forms.ModelForm):
    '''ES作成のためのフォーム'''
    class Meta:
        model = ESGroupModel
        fields = (
            'company',
            'event_type',
            'company_url',
            'is_editing',
            'deadline_date',
            # 'author',
        )


class CreatePostForm(forms.ModelForm):
    '''ポスト作成のためのフォーム'''
    class Meta:
        model = PostModel
        fields = (
            'question',
            'answer',
            'tags',
            'char_num',
            'es_group_id',
        )
