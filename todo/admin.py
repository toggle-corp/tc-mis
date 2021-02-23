from django.contrib import admin

from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    exclude = ['created_by']
    ordering = ('completed', 'created_at')

    def get_queryset(self, request):
        return Todo.objects.filter(created_by=request.user)


admin.site.register(Todo, TodoAdmin)
