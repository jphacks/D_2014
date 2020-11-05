from django import forms

class ChangeColorForm(forms.Form):
    content = forms.CharField(
        label='ES',
        max_length=200,
        required=False,
        widget=forms.Textarea,
    )