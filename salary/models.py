from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from employee.models import Employee


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="employee_salary")
    basic_salary = models.DecimalField(max_digits=9, decimal_places=2)
    allowance = models.DecimalField(max_digits=9, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2, help_text="Calculate in % .")
    gross_salary = models.DecimalField(max_digits=9, decimal_places=2)
    net_salary = models.DecimalField(max_digits=9, decimal_places=2)
    effective_date = models.DateTimeField()

    def __str__(self):
        return f'{self.employee.fullname} - NRs {self.net_salary}'


def pre_salary_created_signal(sender, instance, *args, **kwargs):
    net_salary = (instance.basic_salary + instance.allowance + instance.gross_salary) * instance.tax / 100
    instance.net_salary = net_salary


def post_salary_created_signal(sender, instance, created, **kwargs):
    if created:
        content = f'Your salary has been effective from {instance.effective_date}'
        html_content = render_to_string("salary_email_template.html", {'data': instance, 'content': content})
        subject = f'Salary Review - {instance.employee.fullname}'
        text_content = strip_tags(html_content)
        send_salary_email(subject, text_content, instance.employee.email, html_content)


def send_salary_email(subject, content, to, html_content):
    try:
        email = EmailMultiAlternatives(
            subject,
            content,
            None,
            [to]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


pre_save.connect(pre_salary_created_signal, sender=Salary)
post_save.connect(post_salary_created_signal, sender=Salary)
