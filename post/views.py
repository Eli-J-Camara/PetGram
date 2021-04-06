from django.shortcuts import render, redirect
from post.models import Post
from post.forms import PostForm
from notification.models import Notification
from user_profile.models import CustomUser
import re

from django.core.files.storage import FileSystemStorage

def homepage(request):
    return render(request, 'homepage.html')

# def post_view(request):
#     if request.method == 'POST':
#         uploaded_file = request.FILES['document']
#         # print(uploaded_file.name)
#         # print(uploaded_file.size)
#         fs = FileSystemStorage()
#         fs.save(uploaded_file.name, uploaded_file)
#     return render(request, 'upload_form.html')
def post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = PostForm()
    return render(request, 'upload_form.html', {'form': form})

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'post_detail.html', {'post': post})