from post.models import Post
from user_profile.models import CustomUser
from .forms import ProfileForm
# from authentication.forms import SignUpForm
from django.shortcuts import HttpResponseRedirect,render, reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def homepage(request):
    return render(request, 'homepage.html')

def profile_view(request, user_id):
    context = {}
    user = CustomUser.objects.get(id=user_id)
    form = ProfileForm()
    
    if request.method == 'POST':
        
       
        form = ProfileForm(request.POST)
        
        print(form.errors)
        if form.is_valid():
            print('myformisvalid')
            data = form.cleaned_data
            print(data['display_name'])
            user.bio = data['bio']
            user.display_name = data['display_name']
            user.website = data['website']
            user.save()
            return HttpResponseRedirect(reverse('profile', kwargs={'user_id':user.id}))

    form = ProfileForm(
        initial={'website': user.website, 'bio':user.bio, 'display_name':user.display_name,}
    )

       
    context = {'user': user,'form': form}
    return render(request, 'profile.html', context)




    
    
      


            


