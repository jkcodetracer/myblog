from django.contrib import admin
from .models import Tag,Article,Category

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_time', 'modified_time', 'category', 'author']

# Register your models here.
admin.site.register(Tag)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
