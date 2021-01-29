from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.db import models
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import format_html, strip_tags
from django_currentuser.middleware import get_current_authenticated_user
from django_enumfield import enum

from employee.models import Employee


class SendEmail:
    @staticmethod
    def send_mail(subject, content, from_email, to_email, html_content):
        admin_employee = Employee.objects.filter(is_superuser=1, is_active=1).exclude(id=get_current_authenticated_user().id)
        hr_list = [h.email for h in admin_employee]
        to = hr_list
        to.append(to_email)
        try:
            email = EmailMultiAlternatives(
                subject,
                content,
                from_email,
                [to]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')


class LeaveRequest(models.Model):
    class STATUSES(enum.Enum):
        INACTIVE = 0
        ACTIVE = 1

    class LEAVETYPES(enum.Enum):
        ANNUAL_LEAVE = 0
        SICK_LEAVE = 1
        BEREAVEMENT_LEAVE = 2
        OTHERS = 3

    class LEAVEDETAILS(enum.Enum):
        FULL_DAY = 0
        FIRST_HALF = 1
        SECOND_HALF = 2

    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name="employee")
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = enum.EnumField(LEAVETYPES)
    leave_details = enum.EnumField(LEAVEDETAILS, default=LEAVEDETAILS.FULL_DAY)
    request_to = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name="request_to")
    reason_for_leave = models.CharField(max_length=500, blank=True, null=True)
    status = enum.EnumField(STATUSES, blank=True, null=True)
    verified_by = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name="verified_by", blank=True,
                                    null=True)
    decline_reasons = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reason_for_leave

    def header_status(self):
        if self.status == 0:
            return format_html("<p id='reject_status' title='Reject'>R<p>")
        return format_html("<p id='approve_status' title='Approve'>A<p>")

    header_status.short_description = 'status'

    def save(self, *args, **kwargs):

        # Insert data
        if self.id is None:
            self.employee = get_current_authenticated_user()
            from_username = get_current_authenticated_user()
            content = "I request you to consider my leave application of  {leave_type} from {start_date} to {end_date}" \
                .format(leave_type=self.leave_type, start_date=self.start_date, end_date=self.end_date)
            html_content = render_to_string("email_template.html", {'name': from_username, 'content': content})

            subject = "{from_username} has requested of {sick_leave} from {start_date} to {end_date}".format(
                from_username=from_username, sick_leave=self.leave_type, start_date=self.start_date,
                end_date=self.end_date)
            text_content = strip_tags(html_content)
            SendEmail.send_mail(subject, text_content, from_username, self.request_to.email, html_content)

        return super(LeaveRequest, self).save(*args, **kwargs)
