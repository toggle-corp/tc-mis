from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render

from department.models import Department
from employee.models import Employee


def index(request):
    employee_departments = Department.objects.annotate(
        employee_count=Count(
            'employee_department',
            filter=Q(employee_department__is_active=True)
        )
    )
    employees = Employee.objects.filter(is_active=True).exclude(department__isnull=True).order_by('-join_date')
    context = {
        "employee_departments": employee_departments,
        "employees": employees,
        "title": "ToggleCorp Solutions Pvt. Ltd."
    }

    return render(request, "changelist.html", context)
