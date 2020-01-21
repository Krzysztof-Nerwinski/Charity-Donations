from django.contrib import admin
from donations.models import Institution


def get_categories(obj):
    return ", ".join([cat.name for cat in obj.categories.all()])


get_categories.short_description = "Kategorie"

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', get_categories)

