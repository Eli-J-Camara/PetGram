from django.shortcuts import render
from user_profile.models import CustomUser

def search_bar(request):
    if request.method == 'POST':
        search = request.POST['search']
        users = CustomUser.objects.filter(username__contains=search)
        return render(request, 'search_bar.html', {'search': search, 'users': users})
    else:
         return render(request, 'search_bar.html', {})

