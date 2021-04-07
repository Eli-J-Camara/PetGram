from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, reverse
from post.models import Post
# from post.models import likes
from post.forms import PostForm
from user_profile.models import CustomUser

from django.core.files.storage import FileSystemStorage

def homepage(request):
    return render(request, 'homepage.html')

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



def like_view(request, post_id):
    post = Post.objects.get(id=post_id)
    post.user_likes.add(request.user)
    post.likes += 1
    post.save()
    return HttpResponseRedirect(f'/post_detail/{post.id}')


def unlike_view(request, post_id):
    post = Post.objects.get(id=post_id)
    post.user_likes.remove(request.user)
    post.likes -= 1
    post.save()
    return HttpResponseRedirect(f'/post_detail/{post.id}')


def delete_post_view(request, post_id):
    current_post = Post.objects.get(id=post_id)
    current_post.delete()
    return HttpResponseRedirect('/')
  

