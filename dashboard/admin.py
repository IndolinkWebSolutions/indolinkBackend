from django.contrib import admin
from .models import ClientProducts, CompanyProfile

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display=('name', 'company_name', 'company_gst', 'company_iec', 'business_type')

@admin.register(ClientProducts)
class clientProductAdmin(admin.ModelAdmin):
    list_display = ('products_name', 'category', 'description')
