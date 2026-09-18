from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Employer, Candidate, Job, Application


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ("email",)

    list_display = (
        "email",
        "name",
        "role",
        "is_active",
        "is_verified",
        "is_staff",
    )

    list_filter = (
        "role",
        "is_active",
        "is_verified",
        "is_staff",
    )

    search_fields = (
        "email",
        "name",
        "phone",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "last_login",
    )

    fieldsets = (
        (None, {
            "fields": ("email", "password")
        }),
        ("Personal Information", {
            "fields": ("name", "phone")
        }),
        ("Role & Verification", {
            "fields": ("role", "is_verified")
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {
            "fields": (
                "last_login",
                "created_at",
                "updated_at",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "name",
                "phone",
                "role",
                "password1",
                "password2",
                "is_active",
                "is_verified",
                "is_staff",
                "is_superuser",
            ),
        }),
    )


admin.site.register(Employer)
admin.site.register(Candidate)
admin.site.register(Job)
admin.site.register(Application)