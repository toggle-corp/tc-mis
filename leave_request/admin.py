from django.contrib import admin
from .models import LeaveRequest
from employee.models import Employee
import datetime
from django_currentuser.middleware import get_current_authenticated_user


def approve(modeladmin, request, queryset):
    return queryset.update(status=1)


def reject(modeladmin, request, queryset):
    return queryset.update(status=0)


class LeaveRequestAdmin(admin.ModelAdmin):
    fields = [("start_date", 'end_date'), "leave_type",
              "leave_details", "request_to", "reason_for_leave"]
    exclude = ("employee", "status", "verified_by", "decline_reasons")
    actions = ["approve", "reject"]

    def get_form(self, request, obj=None, **kwargs):
        form = super(LeaveRequestAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['start_date'].initial = datetime.datetime.now()
        #
        employee_list = Employee.objects.exclude(
            fullname=get_current_authenticated_user())
        form.base_fields['request_to'].initial = employee_list
        return form

    def has_add_permission(self, request):
        return request.user.is_staff


# Register your models here.
admin.site.register(LeaveRequest, LeaveRequestAdmin)
