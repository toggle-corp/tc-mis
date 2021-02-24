from django.db import models
from django_currentuser.db.models import CurrentUserField


class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = CurrentUserField()


def __str__(self):
    return self.title
