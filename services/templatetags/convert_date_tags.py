from django import template
from ..utils import jalali_converter

register = template.Library()


@register.filter
def convert_to_jalali(value):
    return jalali_converter(value)
