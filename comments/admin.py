from django.contrib import admin
from .models import Comments

class CommentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'create_time']

# Register your models here.
admin.site.register(Comments, CommentsAdmin)
