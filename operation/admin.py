from django.contrib import admin

from employee.models import Employee
from .models import Operation


class OperationAdmin(admin.ModelAdmin):
    ordering = ('status',)
    search_fields = ("name", "taken_by__fullname")

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Operation.objects.all()
        return Operation.objects.filter(taken_by=request.user)

    def get_list_display(self, request):
        list_display = ["name", "created_at"]
        if request.user.is_superuser:
            return list_display + ["taken_by", "status"]
        return list_display

    def get_form(self, request, obj=None, **kwargs):
        form = super(OperationAdmin, self).get_form(request, obj, **kwargs)
        employee_list = Employee.objects.filter(is_active=True).exclude(id=request.user.id)
        form.base_fields['taken_by'].queryset = employee_list
        return form


admin.site.register(Operation, OperationAdmin)
