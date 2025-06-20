from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'completed', 'date')
    list_filter = ('completed', 'date')
    search_fields = ('title', 'user__username')
