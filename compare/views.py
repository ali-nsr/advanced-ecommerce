from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from store.models import Product
from .compare import Compare
from django.utils.safestring import mark_safe



def add_compare(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    data = Compare(request)
    data.add(product=product)
    messages.success(request, mark_safe(f"""
    محصول {product.title} به <a href="/compare">لیست مقایسه</a> اضافه شد.
    """))
    return redirect(request.META.get('HTTP_REFERER'))


def remove_compare(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    data = Compare(request)
    data.remove(product=product)
    messages.success(request, f'محصول {product.title} از لیست مقایسه حذف شد.')
    return redirect(request.META.get('HTTP_REFERER'))


def compare(request):
    data = Compare(request)
    # if compares.compare:
    return render(request, 'compare/compare_page.html', {'compares': data})
    # else:
    #     messages.info(request, 'محصولی در لیست مقایسه برای نمایش وجود ندارد.')
    #     return redirect('/')
