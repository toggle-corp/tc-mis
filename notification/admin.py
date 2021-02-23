from django.contrib import admin

from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    exclude = ["created_by"]

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.register(Notification, NotificationAdmin)
