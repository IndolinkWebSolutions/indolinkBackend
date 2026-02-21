from django.contrib import admin
from .models import User, UserProfile
# Register your models here.

@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display=['id', 'name', 'mobile_number', 'email', 'weekly_lead_limit']