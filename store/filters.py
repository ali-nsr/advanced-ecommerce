import django_filters
from django import forms
from .models import Product


class ProductFilter(django_filters.FilterSet):
    CHOICE_PRICE = {
        ('گران ترین', 'گران ترین'),
        ('ارزان ترین', 'ارزان ترین'),
    }
    CHOICE_CREATE = {
        ('قدیمی ترین', 'قدیمی ترین'),
        ('جدید ترین', 'جدید ترین'),
    }
    DISCOUNT_CHOICE = {
        ('پر تخفیف ترین', 'پر تخفیف ترین'),
        ('کم تخفیف ترین', 'کم تخفیف ترین'),
    }
    SELL_CHOICE = {
        ('پر فروش ترین', 'پر فروش ترین'),
    }
    price_filter = django_filters.ChoiceFilter(choices=CHOICE_PRICE, method='price_filter_method')
    create_filter = django_filters.ChoiceFilter(choices=CHOICE_CREATE, method='create_filter_method')
    discount_filter = django_filters.ChoiceFilter(choices=DISCOUNT_CHOICE, method='discount_filter_method')
    sell_filter = django_filters.ChoiceFilter(choices=SELL_CHOICE, method='sell_filter_method')

    def price_filter_method(self, queryset, name, value):
        data = 'unit_price' if value == 'ارزان ترین' else '-unit_price'
        return queryset.order_by(data)

    def create_filter_method(self, queryset, name, value):
        data = 'created_date' if value == 'قدیمی ترین' else '-created_date'
        return queryset.order_by(data)

    # def discount_filter_method(self, queryset, name, value):
    #     data = 'discount' if value == 'پر تخفیف ترین' else '-discount'
    #     return queryset.order_by(data)

    def discount_filter_method(self, queryset, name, value):
        if value == 'پر تخفیف ترین':
            data = '-discount'
            return queryset.order_by(data)

    def sell_filter_method(self, queryset, name, value):
        if value == 'پر فروش ترین':
            data = '-sell'
            return queryset.order_by(data)
