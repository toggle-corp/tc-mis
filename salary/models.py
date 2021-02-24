from django.db import models
from django.db.models.signals import pre_save

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


pre_save.connect(pre_salary_created_signal, sender=Salary)
