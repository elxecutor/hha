from django import forms

class NewContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message'}), required=False)
