from django.contrib import admin
from front import models
from django.contrib.auth.admin import UserAdmin
from .models import User

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'category', 'time')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')

admin.site.register(User, UserAdmin)

admin.site.register(models.Category,CategoryAdmin)
admin.site.register(models.Post,PostAdmin)
admin.site.register(models.SocialAccounts)
admin.site.register(models.Comment)
