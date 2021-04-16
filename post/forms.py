from django import forms
from django.forms import ModelForm
from post.models import Post

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('post_file', 'caption')
    
class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

