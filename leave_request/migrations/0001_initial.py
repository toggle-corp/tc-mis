# Generated by Django 3.1.5 on 2021-01-26 06:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields
import leave_request.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('leave_type', django_enumfield.db.fields.EnumField(enum=leave_request.models.LeaveRequest.LeaveTypes)),
                ('leave_details', django_enumfield.db.fields.EnumField(default=0, enum=leave_request.models.LeaveRequest.LeaveDetails)),
                ('reason_for_leave', models.CharField(blank=True, max_length=500, null=True)),
                ('status', django_enumfield.db.fields.EnumField(blank=True, enum=leave_request.models.LeaveRequest.STATUSES, null=True)),
                ('decline_reasons', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='employee', to=settings.AUTH_USER_MODEL)),
                ('request_to', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='request_to', to=settings.AUTH_USER_MODEL)),
                ('verified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='verified_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('leave_request.leaverequest',),
        ),
    ]
