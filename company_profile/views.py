from django.db.models import Count
from django.shortcuts import render

from employee.models import Employee


def index(request):
    employees = Employee.objects.values('department').annotate(count=Count('id')).filter(is_active=True)
    context = {
        "employees": employees
    }

    return render(request, "changelist.html", context)
