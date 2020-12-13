from django import forms
from ..models import PostModel, ESGroupModel


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
    can_delete=False
)
