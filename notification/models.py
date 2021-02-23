from django.db import models
from django_currentuser.db.models import CurrentUserField


class Notification(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    files = models.FileField(upload_to='files/notifications/', blank=True, null=True)
    created_by = CurrentUserField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
