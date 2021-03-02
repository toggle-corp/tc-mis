from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.db import models
from django.db import transaction
from django.db.models.signals import post_save
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

    def save(self, *args, **kwargs):
        self.net_salary = (self.basic_salary + self.allowance + self.gross_salary) * self.tax / 100
        return super(Salary, self).save(*args, **kwargs)


def post_salary_created_signal(sender, instance, created, **kwargs):
    if created:
        content = f'Your salary has been effective from {instance.effective_date}'
        html_content = render_to_string("salary_email_template.html", {'data': instance, 'content': content})
        subject = f'Salary Review - {instance.employee.fullname}'
        text_content = strip_tags(html_content)
        transaction.on_commit(lambda: send_salary_email(
            subject,
            text_content,
            instance.employee.email,
            html_content
        ))


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


post_save.connect(post_salary_created_signal, sender=Salary)
