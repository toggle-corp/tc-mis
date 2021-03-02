from django.contrib import admin

from employee.models import Employee
from .models import Salary


class SalaryAdmin(admin.ModelAdmin):
    list_display = ["employee", 'basic_salary', "allowance", "tax", "gross_salary", "net_salary", "effective_date"]
    exclude = ["net_salary"]

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_queryset(self, request):
        if request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(employee=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super(SalaryAdmin, self).get_form(request, obj, **kwargs)
        employee_list = Employee.objects.filter(is_active=True).exclude(id=request.user.id)
        form.base_fields['employee'].queryset = employee_list
        return form


admin.site.register(Salary, SalaryAdmin)
