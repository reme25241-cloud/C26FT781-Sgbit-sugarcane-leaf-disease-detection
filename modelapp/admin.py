from django.contrib import admin
from .models import Scan

@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ("disease_class", "class_key", "severity", "confidence", "timestamp")
    list_filter = ("class_key", "severity")
    search_fields = ("disease_class",)
    ordering = ("-timestamp",)
    readonly_fields = ("timestamp",)