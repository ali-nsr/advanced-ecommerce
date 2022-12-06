from django import template
from store.models import Category
from cart.cart import Cart
from site_seo.models import *

register = template.Library()


@register.inclusion_tag('store/partials/category_partials_desktop.html')
def store_navbar_desktop():
    return {
        'categories': Category.objects.get_published_categories(),
        'parent_categories': Category.objects.filter(parent=None),
    }


@register.inclusion_tag('store/partials/category_navbar_responsive.html', takes_context=True)
def store_navbar_responsive(context):
    request = context['request']
    return {
        'categories': Category.objects.get_published_categories(),
        'cart': Cart(request),
        'site_setting': SiteSetting.objects.first(),
    }

