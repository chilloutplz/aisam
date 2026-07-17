from django.contrib import admin
from .models import Domain, Unit


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ["name", "semester", "order"]
    list_filter = ["semester"]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ["title", "domain", "is_ready", "order"]
    list_filter = ["domain__semester", "domain", "is_ready"]
    search_fields = ["title"]
