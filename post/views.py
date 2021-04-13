from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from post.models import Post, Comment, Hashtags
from post.forms import PostForm, CommentForm
from user_profile.models import CustomUser
from notification.models import Notification, NotifyComment
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify
import re

@login_required
def homepage(request):
    notify = Notification.objects.filter(reciever=request.user, read=False).count()
    cnotify = NotifyComment.objects.filter(reciever=request.user, read=False).count()
    total_notify = notify + cnotify
    current_user = CustomUser.objects.get(id=request.user.id)
    following = current_user.follows.all()
    feed = Post.objects.filter(display_name__id__in=following).order_by('-created_at').all()
    return render(request, 'homepage.html', {'feed': feed, 'total_notify': total_notify})


def error_404_view(request,):
    return render(request, '404.html', status=404)

def error_500_view(request):
    return render(request, '500.html', status=500)

@login_required 
def post_view(request):
    notify = Notification.objects.filter(reciever=request.user, read=False).count()
    cnotify = NotifyComment.objects.filter(reciever=request.user, read=False).count()
    total_notify = notify + cnotify
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_data = Post.objects.create(
                display_name = request.user,
                caption = form.cleaned_data['caption'],
                post_file = form.cleaned_data['post_file'],
            )

            hashtags = re.findall(r'#(\S+)', form.cleaned_data['caption'])
            for item in hashtags:
                tag = slugify(item[0:50])
                new_tag = Hashtags.objects.get_or_create(
                    slug = tag
                )[0]
                new_tag.post.add(new_data)
                new_tag.save()
                print(new_tag)
        
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
    return render(request, 'upload_form.html', {'form': form, 'total_notify':total_notify})


@login_required
def post_detail(request, post_id):
    notify = Notification.objects.filter(reciever=request.user, read=False).count()
    cnotify = NotifyComment.objects.filter(reciever=request.user, read=False).count()
    total_notify = notify + cnotify
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            print(request.user.id)
            data=form.cleaned_data
            commnt = Comment.objects.create(
                comment = data['comment'],
                user = request.user,
                post = post
            )

            notify = re.findall(r'@(\S+)', data['comment'])
            for item in notify:
                user = CustomUser.objects.filter(username=item).first()
                if user:
                    NotifyComment.objects.create(
                        read = False,
                        text = commnt,
                        reciever = user
                    )
                print(notify)
                return redirect(f'/post_detail/{post.id}')
    else: 
        form = CommentForm()
        comments = Comment.objects.filter(post_id=post.id).order_by('-created_at')
        return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form, 'total_notify': total_notify})

@login_required
def comment_delete(request, id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    return redirect(f'/post_detail/{comment.post.id}')

@login_required
def users_feed(request):
    notify = Notification.objects.filter(reciever=request.user, read=False).count()
    cnotify = NotifyComment.objects.filter(reciever=request.user, read=False).count()
    total_notify = notify + cnotify
    tag = Post.objects.all().order_by('-created_at')
    return render(request, 'users_feed.html', {'tag':tag, 'total_notify': total_notify})

@login_required
def hashtag_view(request, slug_id):
    tag = Hashtags.objects.get(slug=slug_id)
    post = tag.post.all().order_by('-created_at')
    return render(request, 'hashtag.html', {'tag':tag, 'post': post})

@login_required
def like_view(request, post_id):
    post = Post.objects.get(id=post_id)
    post.user_likes.add(request.user)
    post.likes += 1
    post.save()
    return HttpResponseRedirect(f'/post_detail/{post.id}')

@login_required
def unlike_view(request, post_id):
    post = Post.objects.get(id=post_id)
    post.user_likes.remove(request.user)
    post.likes -= 1
    post.save()
    return HttpResponseRedirect(f'/post_detail/{post.id}')

@login_required
def delete_post_view(request, post_id):
    current_post = Post.objects.get(id=post_id)
    current_post.delete()
    return HttpResponseRedirect('/')

