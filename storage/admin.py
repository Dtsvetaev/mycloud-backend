from django.contrib import admin

from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'original_name', 'upload_date', 'size')
