from cart.cart import Cart
from compare.compare import Compare
from site_seo.models import SiteSetting
from store.models import Category

def cart(request):
    return {
        'cart': Cart(request),
        'compare': Compare(request),
    }


def header_footer(request):
    return {
        'site_setting': SiteSetting.objects.first(),
        'footer_categories': Category.objects.get_published_categories(),
    }
