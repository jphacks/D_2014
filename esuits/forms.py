from django import forms
from .models import ESGroupModel, PostModel


class CreateESForm(forms.ModelForm):
    '''ES作成のためのフォーム'''
    class Meta:
        model = ESGroupModel
        fields = (
            'company',
            'event_type',
            'company_url',
            'is_editing',
            'author',
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

class AnswerQuestionForm(forms.ModelForm):
    '''ポスト (ESの中の一つの質問) に答えるためのフォーム'''
    class Meta:
        model = PostModel
        fields = (
            'answer',
        )

AnswerQuestionFormSet = forms.inlineformset_factory(
    parent_model=ESGroupModel,
    model=PostModel,
    form=AnswerQuestionForm,
    extra=0,
)
