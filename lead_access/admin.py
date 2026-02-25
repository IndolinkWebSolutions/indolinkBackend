from django.contrib import admin
from .models import UserDecryptedLead

# Register your models here.

@admin.register(UserDecryptedLead)
class DecryptedAdmin(admin.ModelAdmin):
    list_display = ['user', 'lead']