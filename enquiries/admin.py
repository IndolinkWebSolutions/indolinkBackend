from django.contrib import admin

# Register your models here.

from .models import Contact, HomePagePopUp

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email', 'phoneNo', 'date')

@admin.register(HomePagePopUp)
class HomeEnquiry(admin.ModelAdmin):
    list_display =('company_name', 'email', 'phoneNo', 'create_at')
