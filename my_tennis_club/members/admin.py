from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """
    Admin interface for Member model.
    Rails equivalent: ActiveAdmin.register Member

    Django's admin is built-in - no gems needed!
    """
    list_display = ['id', 'firstname', 'lastname', 'email', 'phone', 'joined_date']
    list_filter = ['joined_date']
    search_fields = ['firstname', 'lastname', 'email']
    ordering = ['lastname', 'firstname']
    readonly_fields = ['joined_date']

    fieldsets = (
        ('Personal Information', {
            'fields': ('firstname', 'lastname')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Metadata', {
            'fields': ('joined_date',)
        }),
    )
