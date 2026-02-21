from django.contrib import admin
from .models import Lead, UserLeadAccess

# ==========================
# Inline Admin for Lead Access
# ==========================
class UserLeadAccessInline(admin.TabularInline):
    model = UserLeadAccess
    extra = 0
    readonly_fields = ('user', 'accessed_at')
    can_delete = False
    verbose_name = "User Lead Access"
    verbose_name_plural = "Users who accessed this lead"

# ==========================
# Lead Admin
# ==========================
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'mobile_number', 'location', 'created_at')
    search_fields = ('name', 'company', 'email', 'location')
    list_filter = ('location', 'created_at')
    inlines = [UserLeadAccessInline]

# ==========================
# UserLeadAccess Admin (optional)
# ==========================
@admin.register(UserLeadAccess)
class UserLeadAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'lead', 'accessed_at')
    search_fields = ('user__username', 'lead__name', 'lead__company')
    list_filter = ('accessed_at',)
    readonly_fields = ('accessed_at',)