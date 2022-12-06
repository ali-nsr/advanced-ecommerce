from django import template
from blog.models import BlogCategory

register = template.Library()


@register.inclusion_tag('blog/partials/blog_category_partial.html')
def blog_navbar_partial():
    return {
        'categories': BlogCategory.objects.all(),
        'parent_categories': BlogCategory.objects.filter(parent=None)
    }