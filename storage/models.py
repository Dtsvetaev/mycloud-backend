import uuid

from django.contrib.auth.models import User
from django.db import models


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='user_files/')
    original_name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, blank=True)
    size = models.PositiveIntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)
    last_download = models.DateTimeField(null=True, blank=True)
    special_link = models.UUIDField(default=uuid.uuid4, unique=True)
