from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Topic, Redactor


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience",)
    search_fields = (
        "first_name",
        "last_name",
        "username",
    )
    list_filter = ("years_of_experience",)
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("years_of_experience",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"classes": ("wide",), "fields": ("years_of_experience",)}),
    )
