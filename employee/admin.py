from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Employee, Designation
from .forms import EmployeeCreationForm, EmployeeChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import PermissionsMixin

# Remove fields from fieldset


def remove_from_fieldsets(fieldsets, fields):
    for fieldset in fieldsets:
        for field in fields:
            if field in fieldset[1]['fields']:
                new_fields = []
                for new_field in fieldset[1]['fields']:
                    if not new_field in fields:
                        new_fields.append(new_field)

                fieldset[1]['fields'] = tuple(new_fields)
                break

# Remove fieldsets


def remove_fieldsets(fieldsets, fieldsetname):
    new_fieldsets = []
    for fieldset in fieldsets:
        if fieldset[0] is not fieldsetname:
            new_fieldsets.append(fieldset)
    return new_fieldsets


class EmployeeAdmin(UserAdmin):
    add_form = EmployeeCreationForm
    form = EmployeeChangeForm
    model = Employee
    fieldsets = (
        (None, {'fields': ('fullname', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff',
                                    'is_superuser', 'is_active')}),
        ('Personal Information',
            {
                'fields':
                (
                    'dob',
                    'gender',
                    'phone_number',
                    'address',
                    'pan_no',
                    'citizenship_no',
                    'designation',
                    'picture',
                    'pan_no_document',
                    'citizenship_document',
                    'department',
                )
            }
         ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'fullname',
                'email',
                'password1',
                'password2',
                'dob',
                'gender',
                'phone_number',
                'address',
                'pan_no',
                'citizenship_no',
                'designation',
                'picture',
                'pan_no_document',
                'citizenship_document',
                'department',
                'date_joined',
            )
        }
        ),
    )
    exclude = ("created_by", "updated_by")
    list_display = (
        "picture_tag",
        "fullname",
        "date_joined",
        "designation",
        'department',
        'is_active'
    )
    list_filter = ("designation", "department", "date_joined")
    search_fields = ["fullname"]
    ordering = ('email',)

    def get_queryset(self, request):
        if request.user.is_staff is True and request.user.is_superuser is False:
            return Employee.objects.filter(email=request.user.email)
        return Employee.objects.all()

    def has_add_permission(self, request):
        if request.user.is_staff is True and request.user.is_superuser is False:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_staff is True and request.user.is_superuser is False:
            return False
        return True

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(EmployeeAdmin, self).get_fieldsets(request, obj)
        if not request.user.is_superuser and request.user.groups.filter(name='publisher').count() == 0:
            return remove_fieldsets(fieldsets, 'Permissions')
        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        disabled_fields = set()
        if request.user.is_staff and not request.user.is_superuser:
            disabled_fields |= {
                'designation',
                'department',
                "date_joined"
            }

            for f in disabled_fields:
                if f in form.base_fields:
                    form.base_fields[f].disabled = True

            designation = form.base_fields["designation"]
            designation.widget.can_add_related = False
            designation.widget.can_change_related = False
            designation.widget.can_delete_related = False

            department = form.base_fields["department"]
            department.widget.can_add_related = False
            department.widget.can_change_related = False
            department.widget.can_delete_related = False
        return form


class DesignationAdmin(admin.ModelAdmin):

    # Hiding Model (Example: Designations)
    def get_model_perms(self, request):
        if request.user.is_staff is True and request.user.is_superuser is False:
            return {}
        return {
            'add': self.has_add_permission(request),
            'change': self.has_change_permission(request),
            'delete': self.has_delete_permission(request),
        }


admin.site.unregister(Group)
# Register your models here.
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Designation, DesignationAdmin)
