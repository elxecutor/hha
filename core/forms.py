from django import forms

class NewContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'h-full-width h-remove-bottom'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'h-full-width h-remove-bottom'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message', 'class': 'h-full-width h-remove-bottom'}), required=False)
