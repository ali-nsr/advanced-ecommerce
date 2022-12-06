from django.shortcuts import render, redirect, get_object_or_404
from store.models import *
from .cart import Cart
from .forms import CartAddForm
from django.contrib import messages
from django.views.decorators.http import require_POST


@require_POST
def add_to_cart(request):
    variant_id = request.POST.get('variantId')
    variant = get_object_or_404(Variants, id=variant_id)
    cart = Cart(request)
    form = CartAddForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        cart.add(variant=variant, quantity=data['quantity'])
        messages.success(request, f'محصول {variant.product.title} به سبد خرید شما اضافه شد.')
    return redirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, variant_id):
    variant = get_object_or_404(Variants, id=variant_id)
    cart = Cart(request)
    cart.remove_all(variant=variant)
    messages.success(request, f'محصول {variant.product.title} از سبد خرید شما حذف شد.')
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    total = 0
    qty = 0
    total_price_without_for_single_variant = 0
    total_price_without_discount = 0
    discount_price = 0
    discount = 0
    total_weight = 0
    for data in cart:
        total += int(data['variant'].total_price * data['quantity'])
        total_price_without_discount += int(data['variant'].unit_price * data['quantity'])
        discount_price = total_price_without_discount - total
        discount += data['variant'].discount_variant
        qty += int(data['quantity'])
        total_price_without_for_single_variant += int(data['variant'].unit_price * data['quantity'])
        total_weight += int(data['variant'].product.weight * data['quantity'])

    context = {
        'cart': cart,
        'total_price': total,
        'qty': qty,
        'total_price_without_discount': total_price_without_discount,
        'total_price_without_for_single_variant': total_price_without_for_single_variant,
        'discount_price': discount_price,
        'discount': discount,
        'total_weight': total_weight,
    }
    return render(request, 'cart/cart.html', context)
