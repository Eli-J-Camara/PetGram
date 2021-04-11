from post.models import Post
from user_profile.models import CustomUser
from .forms import ProfileForm
from django.shortcuts import HttpResponseRedirect,render, reverse
from django.contrib.auth.decorators import login_required


@login_required
def homepage(request):
    return render(request, 'homepage.html')

def edit_profile_view(request, user_id):
    context = {}
    user = CustomUser.objects.get(id=user_id)
    form = ProfileForm()
    follows = True if user in request.user.follows.all() else False

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user.website = data['website']
            user.bio = data['bio']
            user.display_name = data['display_name']
            user.save()
            return HttpResponseRedirect(reverse('profile', kwargs={'user_id':user.id}))

    form = ProfileForm(
        initial={
            'website': user.website,
            'bio':user.bio,
            'display_name':user.display_name,
         }
    )

    context = {'user': user, 'form': form, 'follows': follows}
    return render(request, 'edit_profile.html', context) 

@login_required
def follow_view(request, user_id):
    user = request.user
    to_follow = CustomUser.objects.get(id=user_id)
    user.follows.add(to_follow)
    user.save()
    print('followed')
    # return HttpResponseRedirect('/')
    return HttpResponseRedirect(reverse('profile', kwargs={'user_id':to_follow.id}))

@login_required
def unfollow_view(request, user_id):
    user = request.user
    to_unfollowed = CustomUser.objects.get(id=user_id)
    user.follows.remove(to_unfollowed)
    user.save()
    print('unfollow')
    # return HttpResponseRedirect('/')   
    return HttpResponseRedirect(reverse('profile', kwargs={'user_id': to_unfollowed.id}))   

def profile_view(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    follow_count = user.follows.count() - 1
    return render(request, 'profile.html', {'user': user, 'follow_count': follow_count})

def search_bar(request):
    if request.method == 'POST':
        search = request.POST['search']
        users = CustomUser.objects.filter(username__contains=search)
        return render(request, 'search_bar.html', {'search': search, 'users': users})
    else:
         return render(request, 'search_bar.html', {})

