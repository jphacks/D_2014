from django import forms
from ..models import EntrySheetesModel, QuestionModel, TagModel


class CreateEntrySheetForm(forms.ModelForm):
    '''ES作成のためのフォーム'''
    class Meta:
        model = EntrySheetesModel
        fields = (
            'company',
            'homepage_url',
            'selection_type',
            'is_editing',
            'deadline_date',
            # 'author',
        )


class CreateQuestionForm(forms.ModelForm):
    '''質問作成のためのフォーム'''
    class Meta:
        model = QuestionModel
        fields = (
            'question',
            'answer',
            'tags',
            'is_open',
        )

    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        available_tags = TagModel.objects.filter(authors=user)
        self.fields['tags'].queryset = available_tags
