from django import forms
from django.db.models.enums import Choices
from django.forms import ModelForm
from user_profile.models import CustomUser

CHOICES = (
        ('DG', 'Dog'),
        ('CT', 'Cat'),
        ('HS', 'Hamster'),
        ('BS', 'Bird'),
        ('FS', 'Fish'),
        ('RE', 'Reptile'),
        ('OS', 'Others'),
)

class SignUpForm(forms.Form):
    display_name = forms.CharField(max_length=40)
    pet_type = forms.ChoiceField(choices= CHOICES)
    username = forms.CharField(max_length=40)
    bio = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)



class LoginForm(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(widget=forms.PasswordInput)




# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'password')
#         widgets = {
#             'password': forms.PasswordInput(render_value=True),
#         }