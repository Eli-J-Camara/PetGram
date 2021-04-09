from django.db import models
from django.utils import timezone
from user_profile.models import CustomUser
from tagulous.models import TagField
from django.core.validators import FileExtensionValidator

class Post(models.Model):
    display_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_file= models.FileField(upload_to='post/', validators=[FileExtensionValidator(['jpg','jpeg','mp4', 'mov'])], null=True)
    # post_vid= models.FileField(upload_to='video/', null=True, blank=True)
    caption = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    tags = TagField()

    def __str__(self):
        return f'{self.display_name} | {self.caption}'