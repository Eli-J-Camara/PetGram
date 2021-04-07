from django import forms
from .models import CustomUser

class  ProfileForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ("website", "bio", "display_name", "profile_pic")
