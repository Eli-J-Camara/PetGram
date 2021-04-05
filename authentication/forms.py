from django import forms
from django.forms import ModelForm
from user_profile.models import CustomUser

class SignUpForm(forms.Form):
    display_name = forms.CharField(max_length=40)
    username = forms.CharField(max_length=40)
    bio = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }