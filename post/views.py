from django.shortcuts import render, redirect, reverse
from post.models import Post
from post.forms import PostForm
from user_profile.models import CustomUser
from notification.models import Notification
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import re

@login_required
def homepage(request):
    notify = Notification.objects.filter(reciever=request.user, read=False).count()
    return render(request, 'homepage.html', {'notify': notify})

@login_required
def post_view(request):
    notify = Notification.objects.filter(reciever=request.user, read=False).count()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_data = Post.objects.create(
                display_name = request.user,
                caption = form.cleaned_data['caption'],
                post_file = form.cleaned_data['post_file'],
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
    return render(request, 'post_detail.html', {'post': post})

def users_feed(request):
    notify = Notification.objects.filter(reciever=request.user, read=False).count()
    tag = Post.objects.all().order_by('-created_at')
    return render(request, 'users_feed.html', {'tag':tag, 'notify': notify})

def hashtag_view(request, tag_id):
    tag = Post.objects.filter(tags=tag_id)
    return render(request, 'hashtag.html', {'tag':tag})