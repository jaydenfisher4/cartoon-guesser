from django import forms
from .models import CartoonSuggestion, Show

class CartoonSuggestionForm(forms.ModelForm):
    suggestion_type = forms.ChoiceField(
        choices=CartoonSuggestion.SUGGESTION_TYPES,
        widget=forms.Select(attrs={'onchange': 'toggleFields()'})
    )
    existing_show = forms.ModelChoiceField(
        queryset=Show.objects.all(),
        required=False,
        empty_label="Select a show"
    )

    class Meta:
        model = CartoonSuggestion
        fields = ['suggestion_type', 'show_name', 'existing_show', 'character_name', 'feedback', 'description']
        widgets = {
            'show_name': forms.TextInput(attrs={'placeholder': 'Enter show name'}),
            'character_name': forms.TextInput(attrs={'placeholder': 'Enter character name'}),
            'feedback': forms.Textarea(attrs={'placeholder': 'Share your thoughts'}),
            'description': forms.Textarea(attrs={'placeholder': 'Why should this be added or feedback details'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        suggestion_type = cleaned_data.get('suggestion_type')
        show_name = cleaned_data.get('show_name')
        existing_show = cleaned_data.get('existing_show')
        character_name = cleaned_data.get('character_name')
        feedback = cleaned_data.get('feedback')

        if suggestion_type == 'show' and not show_name:
            raise forms.ValidationError("Show name is required for new show suggestions.")
        elif suggestion_type == 'character':
            if not existing_show:
                raise forms.ValidationError("Please select an existing show for character suggestions.")
            if not character_name:
                raise forms.ValidationError("Character name is required for character suggestions.")
        elif suggestion_type == 'feedback' and not feedback:
            raise forms.ValidationError("Feedback is required for site feedback suggestions.")

        return cleaned_data