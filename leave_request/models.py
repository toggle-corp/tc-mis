from django.db import models
from employee.models import Employee
from django_currentuser.db.models import CurrentUserField
# Create your models here.


class LeaveRequest(models.Model):
    STATUSES = (
        (0, 'Inactive'),
        (1, 'Active'),
    )

    LEAVETYPES = (
        ('annual_leave', 'Annual Leave'),
        ('sick_leave', 'Sick Leave'),
        ('bereavement_leave', 'Bereavement Leave'),
        ('others', 'Others'),
    )

    LEAVEDETAILS = (
        ('full_day', 'Full Day'),
        ('first_half', 'First Half'),
        ('second_half', 'Second Half'),
    )

    employee = models.ForeignKey(
        Employee, on_delete=models.DO_NOTHING, related_name="employee")
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=255, choices=LEAVETYPES)
    leave_details = models.CharField(
        max_length=255, choices=LEAVEDETAILS, default=LEAVEDETAILS[0][0])
    request_to = models.ForeignKey(
        Employee, on_delete=models.DO_NOTHING, related_name="request_to"
    )
    reason_for_leave = models.CharField(max_length=500, blank=True)
    status = models.IntegerField(choices=STATUSES, default=0)
    verified_by = models.ForeignKey(
        Employee, on_delete=models.DO_NOTHING, related_name="verified_by", blank=True
    )
    decline_reasons = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee

     # Save Leave Request
    def save(self,  *args, **kwargs):
        # Insert data
        # if self.id is None:
        # self.employee =
        # self.verified_by =
        return super(LeaveRequest, self).save(*args, **kwargs)
