from django.db import models
from django_enumfield import enum

from employee.models import Employee


class LeaveRequest(models.Model):
    class STATUSES(enum.Enum):
        Inactive = 0
        Active = 1

    class LEAVETYPES(enum.Enum):
        ANNUAL_LEAVE = 0
        SICK_LEAVE = 1
        BEREAVEMENT_LEAVE = 2
        OTHERS = 3

    class LEAVEDETAILS(enum.Enum):
        FULL_DAY = 0
        FIRST_HALF = 1
        SECOND_HALF = 2

    employee = models.ForeignKey(
        Employee, on_delete=models.DO_NOTHING, related_name="employee")
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = enum.EnumField(LEAVETYPES)
    leave_details = enum.EnumField(LEAVEDETAILS, default=LEAVEDETAILS.FULL_DAY)
    request_to = models.ForeignKey(
        Employee, on_delete=models.DO_NOTHING, related_name="request_to"
    )
    reason_for_leave = models.CharField(max_length=500, blank=True, null=True)
    status = enum.EnumField(STATUSES, blank=True, null=True)
    verified_by = models.ForeignKey(
        Employee, on_delete=models.DO_NOTHING, related_name="verified_by", blank=True, null=True
    )
    decline_reasons = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee

    def save(self, *args, **kwargs):
        # Insert data
        # if self.id is None:
        # self.employee =
        # self.verified_by =
        return super(LeaveRequest, self).save(*args, **kwargs)
