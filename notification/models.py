from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.db import models
from django.db.models.signals import post_save
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_currentuser.db.models import CurrentUserField

from employee.models import Employee


class Notification(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='file/notifications/', blank=True, null=True)
    file_type = models.CharField(null=True, blank=True, max_length=100)
    created_by = CurrentUserField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.file_type = self.files.file.content_type
        super().save(*args, **kwargs)


def post_notification_created_signal(sender, instance, created, **kwargs):
    if created:
        content = instance.description
        html_content = render_to_string("notification_email_template.html", {'content': content})
        subject = instance.title
        text_content = strip_tags(html_content)
        send_notification(subject, text_content, html_content, instance.files, instance.content_type)


def send_notification(subject, content, html_content, files, file_content_type):
    employee_list = Employee.objects.filter(is_active=True, is_superuser=False)
    email_list = [h.email for h in employee_list]
    try:
        email = EmailMultiAlternatives(
            subject,
            content,
            None,
            email_list
        )
        if files:
            email.attach(files.name, files.read(), file_content_type)
        email.attach_alternative(html_content, "text/html")
        email.send()
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


post_save.connect(post_notification_created_signal, sender=Notification)
