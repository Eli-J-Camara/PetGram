from django import forms
from django.forms import ModelForm
from user_profile.models import CustomUser
from django.core.exceptions import ValidationError

class SignUpForm(forms.Form):
    display_name = forms.CharField(max_length=40)
    username = forms.CharField(max_length=40)
    bio = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_query = CustomUser.objects.filter(username=username)
        if user_query.exists():
            raise forms.ValidationError('Username already exists')
        return username


class LoginForm(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(widget=forms.PasswordInput)
