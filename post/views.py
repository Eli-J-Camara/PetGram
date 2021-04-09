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
    notify = Notification.objects.filter(reciever=request.user, read=False).count()
    current_user = CustomUser.objects.get(id=request.user.id)
    following = current_user.follows.all()
    feed = Post.objects.filter(display_name__id__in=following).order_by('-created_at').all()
    return render(request, 'homepage.html', {'feed': feed, 'notify': notify})

@login_required 
def post_view(request):
    notify = Notification.objects.filter(reciever=request.user, read=False).count()
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
    return render(request, 'upload_form.html', {'form': form, 'notify': notify})


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
    notify = Notification.objects.filter(reciever=request.user, read=False).count()
    tag = Post.objects.all().order_by('-created_at')
    return render(request, 'users_feed.html', {'tag':tag, 'notify': notify})

def hashtag_view(request, tag_id):
    tag = Post.objects.filter(tags=tag_id)
    return render(request, 'hashtag.html', {'tag':tag})


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

