from django import forms

class NewsAPIForm(forms.Form):
    content = forms.CharField(
        label='ES',
        max_length=200,
        required=False,
    )
    
    name = forms.CharField(
        label='会社名',
        max_length=200,
        required=False,
    )
