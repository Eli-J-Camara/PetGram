from django.shortcuts import render
from post.models import Post
from post.forms import PostForm

from django.core.files.storage import FileSystemStorage

def homepage(request):
    return render(request, 'homepage.html')

def post_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        # print(uploaded_file.name)
        # print(uploaded_file.size)
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
    return render(request, 'upload_form.html')