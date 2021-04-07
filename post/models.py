from django.db import models
from django.utils import timezone
from user_profile.models import CustomUser


class Post(models.Model):
    display_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fullname')
    post_pic = models.ImageField(upload_to='post_img/', null=True)
    caption = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    user_likes = models.ManyToManyField(CustomUser, symmetrical=False, default=CustomUser, blank=True)
    # dislikes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.display_name} | {self.caption}'


