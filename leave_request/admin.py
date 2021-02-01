from django.contrib import admin
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import format_html, strip_tags

from employee.models import Employee
from .models import LeaveRequest, SendEmail


class LeaveRequestAdmin(admin.ModelAdmin):
    fields = [("start_date", 'end_date'), "leave_type",
              "leave_details", "request_to", "reason_for_leave"]
    exclude = ("employee", "status", "verified_by", "decline_reasons")

    def get_list_display(self, request):
        list_display = ["start_date", 'end_date', "leave_type", "leave_details", "request_to", "reason_for_leave",
                        "header_status"]
        if request.user.is_superuser:
            return ["employee"] + list_display
        return list_display

    def get_form(self, request, obj=None, **kwargs):
        form = super(LeaveRequestAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['start_date'].initial = timezone.now()
        # Eliminate Login User
        employee_list = Employee.objects.filter(is_active=True, department=request.user.department).exclude(
            id=request.user.id)
        form.base_fields['request_to'].queryset = employee_list
        return form

    def get_queryset(self, request):
        if request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(employee_id=request.user.id)

    def has_add_permission(self, request):
        return not request.user.is_superuser


class Request(LeaveRequest):
    class Meta:
        proxy = True


def approve(modeladmin, request, queryset):
    for obj in queryset:
        content = "Your request has been approved from {start_date} to {end_date} ." \
            .format(start_date=obj.start_date, end_date=obj.end_date)
        html_content = render_to_string("email_template.html", {'name': request.user, 'content': content})
        subject = "Your request has been approved."
        text_content = strip_tags(html_content)
        SendEmail.send_mail(subject, text_content, request.user.email, obj.employee.email, html_content)

    queryset.update(status=LeaveRequest.STATUSES.ACTIVE, verified_by_id=request.user.id)


def reject(modeladmin, request, queryset):
    for obj in queryset:
        decline_reasons = obj.decline_reasons or ""
        content = "Your request has been rejected from {start_date} to {end_date}. {decline_reasons}" \
            .format(start_date=obj.start_date, end_date=obj.end_date, decline_reasons=decline_reasons)
        html_content = render_to_string("email_template.html", {'name': request.user, 'content': content})
        subject = "Your request has been rejected."
        text_content = strip_tags(html_content)
        SendEmail.send_mail(subject, text_content, request.user.email, obj.employee.email, html_content)

    queryset.update(status=LeaveRequest.STATUSES.INACTIVE, verified_by_id=request.user.id)


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
