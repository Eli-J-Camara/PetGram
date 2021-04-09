from django.shortcuts import render
from notification.models import Notification
from post.models import Post
from user_profile.models import CustomUser
from django.contrib.auth.decorators import login_required

@login_required
def notification_view(request):
    user = request.user
    notifications = Notification.objects.filter(reciever=user, read=False)
    for alert in notifications:
        alert.read = False
        alert.save()
    return render(request, 'notification.html', {'notifications': notifications})