from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.html import mark_safe
from django_currentuser.db.models import CurrentUserField
from django_enumfield import enum

from department.models import Department
from .managers import EmployeeManager


class Designation(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class UserResourceMixin:
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField()
    updated_by = CurrentUserField(on_update=True)


class Employee(UserResourceMixin, AbstractUser):
    class GENDER(enum.Enum):
        Female = 0
        Male = 1

    username = None
    fullname = models.CharField(max_length=255, verbose_name='Full Name')
    dob = models.DateField(verbose_name='Date of Birth', null=True, blank=True)
    gender = enum.EnumField(GENDER, null=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=16, validators=[
        RegexValidator(
            regex=r'^\+977\s-?\d{10}$',
            message="Phone number must be entered in the format '+977 9999999999'."
        ),
    ], null=True, blank=True, help_text="Phone number must be entered in the format '+977 9999999999'.")
    address = models.CharField(max_length=255, null=True, blank=True)
    pan_no = models.CharField(max_length=255, unique=True, null=True, blank=True)
    citizenship_no = models.CharField(max_length=255, unique=True, null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.PROTECT, null=True, blank=True)
    join_date = models.DateField(auto_now_add=True)
    picture = models.ImageField(upload_to='images/pictures/', blank=True, null=True)
    pan_no_document = models.ImageField(upload_to='images/pans/', blank=True, null=True)
    citizenship_document = models.ImageField(upload_to='images/citizenships/', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='department', null=True)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    objects = EmployeeManager()

    def __str__(self):
        return self.fullname

    def picture_tag(self):
        """
        To display picture in List view
        """
        if self.picture:
            return mark_safe('<img src="%s" width="50" height="50" />' % self.picture.url)
        else:
            return mark_safe(
                '<img src="https://togglecorp.com/favicon.ico" alt="ToggleCorp" title="ToggleCorp" width="50" '
                'height="50"/>')

    picture_tag.short_description = 'Picture'
    picture_tag.allow_tags = True

    def has_module_perms(self, app_label):
        return self.is_superuser or app_label != 'department'

    def has_perm(self, perm, obj=None):
        if perm is 'employee.view_designation':
            return self.is_superuser
        return self.is_staff