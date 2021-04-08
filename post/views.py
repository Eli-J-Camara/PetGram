from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from post.models import Post, Comment
from post.forms import PostForm, CommentForm
from user_profile.models import CustomUser
from notification.models import Notification
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import re

@login_required
def homepage(request):
    feed = Post.objects.all().order_by('-created_at')
    return render(request, 'homepage.html', {'feed': feed})

@login_required 
def post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_data = Post.objects.create(
                display_name = request.user,
                caption = form.cleaned_data['caption'],
                post_pic = form.cleaned_data['post_pic'],
                tags = form.cleaned_data['tags']
            )

            notifications = re.findall(r'@(\S+)', form.cleaned_data['caption'])
            for string in notifications:
                user = CustomUser.objects.filter(username=string).first()
                if user:
                    Notification.objects.create(
                        read = False,
                        text = new_data,
                        reciever = user
                    )
            print(notifications)
            return redirect(reverse('post_detail', args=[new_data.id]))
    else:
        form = PostForm()
    return render(request, 'upload_form.html', {'form': form})


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            print(request.user.id)
            data=form.cleaned_data
            comment = Comment.objects.create(
                comment = data['comment'],
                user = request.user,
                post = post
            )
            return redirect(f'/post_detail/{post.id}')
    form = CommentForm()
    comments = Comment.objects.filter(post_id=post.id).order_by('-created_at')
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

def comment_delete(request, id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    return redirect(f'/post_detail/{comment.post.id}')

def users_feed(request):
    tag = Post.objects.all().order_by('-created_at')
    return render(request, 'users_feed.html', {'tag':tag})

def hashtag_view(request, tag_id):
    tag = Post.objects.filter(tags=tag_id)
    return render(request, 'hashtag.html', {'tag':tag})

