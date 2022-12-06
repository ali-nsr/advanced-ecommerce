from django.contrib import admin
from . import models


class ItemOrderInline(admin.TabularInline):
    model = models.ItemOrder
    # can_delete = False
    extra = 0
    # exclude = ('price', 'variant')


class OrderAdmin(admin.ModelAdmin):
    model = models.Order
    list_display = (
        'user', 'first_name', 'last_name', 'province', 'city', 'phone','total', 'is_paid', 'order_code',
        'jalali_created_date', 'number')
    list_filter = ('is_paid', 'created_date')
    # readonly_fields = (
    #     'user', 'address', 'city', 'province', 'phone', 'first_name', 'last_name', 'status', 'total',
    #     'order_description')
    # can_delete = False
    # exclude = ('shipping_status', 'shipping_cost')
    inlines = [ItemOrderInline]


class ItemOrder(admin.ModelAdmin):
    list_display = ('user', 'quantity')
    # readonly_fields = (
    #     'order', 'user', 'variant', 'unit_price', 'console_guarantee', 'controller_guarantee', 'discount', 'unit_price',
    #     'quantity',
    #     'price')
    # list_filter = ('user',)


admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.ItemOrder, ItemOrder)
