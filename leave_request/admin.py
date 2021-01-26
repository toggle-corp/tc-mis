import datetime

from django.contrib import admin
from django.utils.html import format_html

from employee.models import Employee
from .models import LeaveRequest


class LeaveRequestAdmin(admin.ModelAdmin):
    fields = [("start_date", 'end_date'), "leave_type",
              "leave_details", "request_to", "reason_for_leave"]
    exclude = ("employee", "status", "verified_by", "decline_reasons")

    def get_list_display(self, request):
        if request.user.is_superuser:
            return "employee", "start_date", 'end_date', "leave_type", "leave_details", "request_to", "reason_for_leave", "header_status"
        return "start_date", 'end_date', "leave_type", "leave_details", "request_to", "reason_for_leave", "header_status"

    def get_form(self, request, obj=None, **kwargs):
        form = super(LeaveRequestAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['start_date'].initial = datetime.datetime.now()
        # Eliminate Login User
        employee_list = Employee.objects.exclude(id=request.user.id)
        form.base_fields['request_to'].queryset = employee_list
        return form

    def get_queryset(self, request):
        if request.user.is_superuser:
            self.list_display = "employee"
            return self.model.objects.all()
        return self.model.objects.filter(employee_id=request.user.id)


class Request(LeaveRequest):
    class Meta:
        proxy = True


def approve(modeladmin, request, queryset):
    queryset.update(status=1, verified_by_id=request.user.id)


def reject(modeladmin, request, queryset):
    queryset.update(status=0, verified_by_id=request.user.id)


class RequestAdmin(LeaveRequestAdmin):
    actions = [approve, reject]

    change_list_template = 'list.html'

    def get_list_display(self, request):
        return ("employee", "start_date", 'end_date', "leave_type",
                "leave_details", "request_to", "reason_for_leave", "header_status", "action_btn")

    def get_queryset(self, request):
        if request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(request_to=request.user.id)

    def action_btn(self, obj):
        return format_html(
            "<button class='leave_request_btn' id='approve' value={}>Approve</button>&nbsp;&nbsp;<button class='leave_request_btn' id='reject' value={}>Reject</button>",
            obj.pk, obj.pk
        )

    action_btn.short_description = "Action"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# Register your models here.
admin.site.register(LeaveRequest, LeaveRequestAdmin)
admin.site.register(Request, RequestAdmin)
