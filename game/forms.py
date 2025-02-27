from django import forms
from .models import CartoonSuggestion

class CartoonSuggestionForm(forms.ModelForm):
    class Meta:
        model = CartoonSuggestion
        fields = ['name', 'description']