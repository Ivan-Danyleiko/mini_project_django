from django import forms
from django.forms import TextInput, CharField
from .models import Author, Quote


class AuthorForm(forms.ModelForm):
    fullname = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']
