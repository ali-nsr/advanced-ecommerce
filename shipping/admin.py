from django.contrib import admin
from .models import *


class CitiesInline(admin.TabularInline):
    model = Cities


class ProvincesAdmin(admin.ModelAdmin):
    list_display = ('fa_name',)
    inlines = [CitiesInline]


admin.site.register(Provinces, ProvincesAdmin)
admin.site.register(WeightPrice)
