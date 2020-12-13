from django import forms
from ..models import QuestionModel, EntrySheetesModel


class AnswerQuestionForm(forms.ModelForm):
    '''ポスト (ESの中の一つの質問) に答えるためのフォーム'''
    class Meta:
        model = QuestionModel
        fields = (
            'answer',
        )


AnswerQuestionFormSet = forms.inlineformset_factory(
    parent_model=EntrySheetesModel,
    model=QuestionModel,
    form=AnswerQuestionForm,
    extra=0,
    can_delete=False
)
