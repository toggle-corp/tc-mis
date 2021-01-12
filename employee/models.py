from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
import datetime

# Create your models here.


class Designation(models.Model):
    type = models.CharField(max_length=100)

    class Meta:
        db_table = "designations"

    def __str__(self):
        return self.type


class Employee(models.Model):
    GENDER = (
        (0, 'Female'),
        (1, 'Male'),
    )
    STATUSES = (
        (0, 'Inactive'),
        (1, 'Active'),
    )
    fullname = models.CharField(max_length=255, verbose_name='Full Name')
    dob = models.DateField(verbose_name='Date of Birth')
    gender = models.IntegerField(choices=GENDER)
    email = models.EmailField(max_length=255, unique=True)
    pan_no = models.CharField(max_length=255, unique=True)
    citizenship_no = models.CharField(max_length=255, unique=True)
    designation = models.ForeignKey(
        Designation, on_delete=models.DO_NOTHING)
    join_date = models.DateField()
    picture = models.ImageField(upload_to='pictures/')
    status = models.IntegerField(choices=STATUSES)
    createdBy = models.PositiveIntegerField()
    updatedBy = models.PositiveIntegerField()
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "employees"

    def __str__(self):
        return self.fullname

    # To display picture in List view
    def picture_tag(self):
        if self.picture:
            return mark_safe('<img src="%s" width="150" height="150" />' % (self.picture))
        else:
            return mark_safe(
                '<img src="https://togglecorp.com/favicon.ico" alt="ToggleCorp" title="ToggleCorp" width="50" height="50"/>')
    picture_tag.allow_tags = True
    picture_tag.short_description = 'Picture'

    # Save Employee Data
    def save(self,  *args, **kwargs):
        if self.createdBy:
            self.updatedBy = 20
            self.updatedAt = datetime.datetime.now()
        else:
            self.createdBy = 20
            self.updatedBy = 20
        super(Employee, self).save(*args, **kwargs)
