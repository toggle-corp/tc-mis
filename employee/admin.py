from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Employee, Designation


class EmployeeAdmin(admin.ModelAdmin):
    exclude = ("createdBy", "updatedBy")
    list_display = ("picture_tag", "fullname", "join_date",  "designation")
    list_filter = ("designation", "join_date")
    search_fields = ["fullname"]


admin.site.unregister(Group)
# Register your models here.
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Designation)
