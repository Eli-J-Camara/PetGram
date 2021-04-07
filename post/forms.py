from django import forms
from django.forms import ModelForm
from post.models import Post

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('post_pic', 'caption')
    
class CommentForm(forms.Form):
    comment = forms.CharField()
