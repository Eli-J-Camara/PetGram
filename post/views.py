from django.shortcuts import render
from post.models import Post
from post.forms import PostForm

def homepage(request):
    return render(request, 'homepage.html')

def post_view(request):
    context = {}
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            data = form.cleaned_data
            new_post = Post.objects.create(
                post_pic = data['post_pic'],
                caption = data['caption']
            )
            return redirect('post_detail')
    form = PostForm()
    context.update({'form': form})
    return render(request, 'generic_form.html', context)