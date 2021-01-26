# Generated by Django 3.1.5 on 2021-01-25 10:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='cititzen_document',
            field=models.ImageField(upload_to='images/citizenships/'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='pan_no_document',
            field=models.ImageField(upload_to='images/pans/'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone_number',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format '+977 9999999999'.", regex='^\\+977\\s-?\\d{10}$')]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='picture',
            field=models.ImageField(upload_to='images/pictures/'),
        ),
    ]
