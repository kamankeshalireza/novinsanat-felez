from django.contrib import admin

from website.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin interface for managing contact form submissions."""

    date_hierarchy = "created_at"
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)
