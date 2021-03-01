from django.db import models
from django_currentuser.db.models import CurrentUserField


class ExpenseClaim(models.Model):
    name = models.CharField(max_length=100)
    remarks = models.TextField()
    picture = models.ImageField(upload_to='images/expense_claim/', blank=True, null=True)
    is_approve = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = CurrentUserField()

    def __str__(self):
        return self.name
