from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe
from django_currentuser.middleware import get_current_authenticated_user

from department.models import Department
from .managers import EmployeeManager


# Create your models here.


class Designation(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class Employee(AbstractUser):
    username = None
    GENDER = (
        (0, 'Female'),
        (1, 'Male'),
    )

    fullname = models.CharField(max_length=255, verbose_name='Full Name')
    dob = models.DateField(verbose_name='Date of Birth', null=True, blank=True)
    gender = models.IntegerField(choices=GENDER, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=16, validators=[
        RegexValidator(
            regex=r'^\+977\s-?\d{10}$',
            message="Phone number must be entered in the format '+977 9999999999'."
        ),
    ], null=True, blank=True, help_text="Phone number must be entered in the format '+977 9999999999'.")
    address = models.CharField(max_length=255, null=True, blank=True)
    pan_no = models.CharField(
        max_length=255, unique=True, null=True, blank=True)
    citizenship_no = models.CharField(
        max_length=255, unique=True, null=True, blank=True)
    designation = models.ForeignKey(
        Designation, on_delete=models.PROTECT, null=True, blank=True)
    join_date = models.DateField(default=timezone.now)
    picture = models.ImageField(
        upload_to='images/pictures/', blank=True, null=True)
    pan_no_document = models.ImageField(
        upload_to='images/pans/', blank=True, null=True)
    citizenship_document = models.ImageField(
        upload_to='images/citizenships/', blank=True, null=True
    )
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name='department', null=True
    )
    is_staff = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        'self', on_delete=models.PROTECT, related_name="who_created", blank=True, null=True
    )
    updated_by = models.ForeignKey(
        'self', on_delete=models.PROTECT, related_name="who_updated", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    objects = EmployeeManager()

    def __str__(self):
        return self.fullname

    # To display picture in List view
    @property
    def picture_tag(self):
        if self.picture:
            return mark_safe('<img src="%s" width="50" height="50" />' % self.picture.url)
        else:
            return mark_safe(
                '<img src="https://togglecorp.com/favicon.ico" alt="ToggleCorp" title="ToggleCorp" width="50" '
                'height="50"/>')

    picture_tag.short_description = 'Picture'
    picture_tag.allow_tags = True

    # Save Employee Data
    def save(self, *args, **kwargs):
        # Update data
        if self.id:
            self.updated_by = get_current_authenticated_user()
        # Insert data
        else:
            self.created_by = get_current_authenticated_user()
            self.updated_by = get_current_authenticated_user()
        super(Employee, self).save(*args, **kwargs)

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        else:
            if app_label == 'department':
                return False
        return True
