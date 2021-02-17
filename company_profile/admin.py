from django.contrib import admin
from django.urls import path

from .models import CompanyProfile
from .views import index


class CompanyProfileAdmin(admin.ModelAdmin):
    def get_urls(self):
        view_name = f"{self.model._meta.app_label}_{self.model._meta.model_name}_changelist"
        return [
            path('', index, name=view_name),
        ]


admin.site.register(CompanyProfile, CompanyProfileAdmin)
