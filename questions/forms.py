from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        widgets = {
            'question_text': forms.Textarea(attrs={
                'placeholder': 'Your Question',
                'class': 'h-full-width h-remove-bottom'
            }),
        }