from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.db import models
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import format_html, strip_tags
from django.utils.translation import ugettext_lazy
from django_currentuser.db.models import CurrentUserField
from django_currentuser.middleware import get_current_authenticated_user
from django_enumfield import enum

from employee.models import Employee


class SendEmail:
    @staticmethod
    def send_mail(subject, content, from_email, to_email, html_content):
        admin_employee = Employee.objects.filter(is_superuser=True, is_active=True).exclude(
            id=get_current_authenticated_user().id)
        hr_list = [h.email for h in admin_employee]
        to = hr_list
        to.append(to_email)
        try:
            email = EmailMultiAlternatives(
                subject,
                content,
                from_email,
                to
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')


class LeaveRequest(models.Model):
    class Statuses(enum.Enum):
        INACTIVE = 0
        ACTIVE = 1

    class LeaveTypes(enum.Enum):
        ANNUAL_LEAVE = 0
        SICK_LEAVE = 1
        BEREAVEMENT_LEAVE = 2
        OTHERS = 3

        __labels__ = {
            ANNUAL_LEAVE: ugettext_lazy("Annual Leave"),
            SICK_LEAVE: ugettext_lazy("Sick Leave"),
            BEREAVEMENT_LEAVE: ugettext_lazy("Bereavement Leave"),
            OTHERS: ugettext_lazy("Others"),
        }

    class LeaveDetails(enum.Enum):
        FULL_DAY = 0
        FIRST_HALF = 1
        SECOND_HALF = 2

        __labels__ = {
            FULL_DAY: ugettext_lazy("Full Day"),
            FIRST_HALF: ugettext_lazy("First Half"),
            SECOND_HALF: ugettext_lazy("Second Half")
        }

    employee = CurrentUserField()
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = enum.EnumField(LeaveTypes)
    leave_details = enum.EnumField(LeaveDetails, default=LeaveDetails.FULL_DAY)
    request_to = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name="request_to")
    reason_for_leave = models.CharField(max_length=500, blank=True, null=True)
    status = enum.EnumField(Statuses, blank=True, null=True)
    verified_by = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name="verified_by", blank=True,
                                    null=True)
    decline_reasons = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reason_for_leave

    def header_status(self):
        if self.status == self.Statuses.INACTIVE:
            return format_html("<p id='reject_status' title='Reject'>R<p>")
        elif self.status == self.Statuses.ACTIVE:
            return format_html("<p id='approve_status' title='Approve'>A<p>")
        else:
            return ""

    header_status.short_description = 'status'

    def save(self, *args, **kwargs):
        # Insert data
        if self.id is None:
            from_username = get_current_authenticated_user()
            content = f"I request you to consider my leave application of  {self.leave_type} from {self.start_date} to {self.end_date}"
            html_content = render_to_string("email_template.html", {'name': from_username, 'content': content})
            subject = f"{from_username} has requested of {self.leave_type} from {self.start_date} to {self.end_date}"
            text_content = strip_tags(html_content)
            SendEmail.send_mail(subject, text_content, from_username, self.request_to.email, html_content)

        return super(LeaveRequest, self).save(*args, **kwargs)
