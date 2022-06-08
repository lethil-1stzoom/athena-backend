from django.contrib import admin
from .models import *

admin.site.register(VideoFiles)
admin.site.register(FileGroups)
admin.site.register(UniqueURL)

class ImageFilesAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'upload_by']

admin.site.register(ImageFiles, ImageFilesAdmin)