# Generated by Django 3.1.5 on 2021-02-23 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='taken_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='operation_taken_by', to=settings.AUTH_USER_MODEL),
        ),
    ]