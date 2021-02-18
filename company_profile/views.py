from django.db.models import Count
from django.shortcuts import render

from employee.models import Employee


def index(request):
    employee_departments = Employee.objects.values('department__name').annotate(count=Count('id')).filter(
        is_active=True).exclude(department__isnull=True)
    employees = Employee.objects.filter(is_active=True).exclude(department__isnull=True).order_by('-join_date')
    context = {
        "employee_departments": employee_departments,
        "employees": employees,
        "title": "ToggleCorp Solutions Pvt. Ltd."
    }

    return render(request, "changelist.html", context)
