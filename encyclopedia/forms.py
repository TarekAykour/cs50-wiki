from logging import PlaceHolder
from django import forms

class SearchForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)