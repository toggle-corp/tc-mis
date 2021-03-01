from django.contrib import admin

from .models import ExpenseClaim


class ExpenseClaimAdmin(admin.ModelAdmin):
    list_display = ("name", "is_approve")

    def get_exclude(self, request, obj=None):
        if not request.user.is_superuser:
            return ['created_by', 'is_approve']
        else:
            return ['created_by']


admin.site.register(ExpenseClaim, ExpenseClaimAdmin)
