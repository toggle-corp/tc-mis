from django.db import models

from employee.models import Employee


class Operation(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    remarks = models.TextField()
    picture = models.ImageField(upload_to='images/operations/', blank=True, null=True)
    status = models.BooleanField(default=True)
    taken_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="operation_taken_by", blank=True,
                                 null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
