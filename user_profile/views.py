from post.models import Post
from user_profile.models import CustomUser
from .forms import ProfileForm
from notification.models import Notification
from django.shortcuts import HttpResponseRedirect,render, reverse
from django.contrib.auth.decorators import login_required



@login_required
def edit_profile_view(request, user_id):
    context = {}
    notify = Notification.objects.filter(reciever=request.user, read=False).count()
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
            user.pet_type = data['pet_type']
            user.save()
            return HttpResponseRedirect(reverse('profile', kwargs={'user_id':user.id}))

    form = ProfileForm(
        initial={
            'website': user.website,
            'bio':user.bio,
            'display_name':user.display_name,
            'pet_type':user.pet_type,
         }
    )

    context = {'user': user, 'form': form, 'follows': follows, 'notify': notify}
    return render(request, 'edit_profile.html', context) 

def error_404_view(request,):
    return render(request, '404.html', status=404)

def error_500_view(request):
    return render(request, '500.html', status=500)

@login_required
def follow_view(request, user_id):
    user = request.user
    to_follow = CustomUser.objects.get(id=user_id)
    user.follows.add(to_follow)
    to_follow.followers.add(user)
    user.save()
    print('followed')
    # return HttpResponseRedirect('/')
    return HttpResponseRedirect(reverse('profile', kwargs={'user_id':to_follow.id}))

@login_required
def unfollow_view(request, user_id):
    user = request.user
    to_unfollowed = CustomUser.objects.get(id=user_id)
    user.follows.remove(to_unfollowed)
    to_follow.followers.remove(user)
    user.save()
    print('unfollow')
    # return HttpResponseRedirect('/')   
    return HttpResponseRedirect(reverse('profile', kwargs={'user_id': to_unfollowed.id}))   

def profile_view(request, user_id):
    # notify = Notification.objects.filter(reciever=request.user, read=False).count()
    user_obj = CustomUser.objects.get(id=user_id)
    post = Post.objects.filter(display_name=user_obj).order_by('-created_at')
    following_count = user_obj.follows.count()
    follower_count = user_obj.followers.count()
    follow_list = user_obj.follows.all()
    return render(request, 'profile.html', {'user': user_obj, 'follow_list':follow_list, 'following_count': following_count, 'follower_count': follower_count, 'post': post})



@login_required
def search_bar(request):
    notify = Notification.objects.filter(reciever=request.user, read=False).count()
    if request.method == 'POST':
        search = request.POST['search']
        users = CustomUser.objects.filter(username__contains=search)
        return render(request, 'search_bar.html', {'search': search, 'users': users})
    else:
         return render(request, 'search_bar.html', {'notify': notify})



