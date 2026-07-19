from django.contrib import admin
from .models import Domain, Unit


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ["name", "subject", "grade", "semester", "order"]
    list_filter = ["subject", "grade", "semester"]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "domain", "is_ready", "order"]
    list_filter = ["domain__subject", "domain__grade", "domain", "is_ready"]
    search_fields = ["title", "slug"]
