from django.db import models


class WallActivity(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.title
