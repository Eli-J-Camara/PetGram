from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from post.models import Post, Comment
from post.forms import PostForm, CommentForm

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

