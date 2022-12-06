from django.contrib import admin
from .models import *


# Register your models here.


class SpecificationsInline(admin.TabularInline):
    model = CompareSpecifications
    extra = 1


class TitlesAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [SpecificationsInline]


admin.site.register(Compare)
admin.site.register(CompareTitle, TitlesAdmin)
