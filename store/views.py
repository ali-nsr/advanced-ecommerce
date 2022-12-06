from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from slider.models import *
from blog.models import Article
from site_seo.models import HomeSeo
from .forms import *
from .filters import ProductFilter
from cart.forms import CartAddForm
from django.core.paginator import Paginator
from django.views.generic import ListView
from urllib.parse import urlencode
from django.contrib import messages
from compare.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def home(request):
    sliders = SliderHome.objects.get_published_sliders()
    offer_sliders = SliderHomeOffer.objects.all()
    when = SliderOfferDate.objects.last()
    context = {
        'sliders': sliders,
        'offer_sliders': offer_sliders,
        'products': Product.objects.get_published_products(),
        'components': Position.objects.all(),
        'when': when,
        'home_seo': HomeSeo.objects.first(),
        'latest_articles': Article.objects.get_active_articles().order_by('-id')[:8]
    }
    return render(request, 'store/home.html', context)


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    product_images = Gallery.objects.filter(product_id=product.id)
    comment_form = CommentForm()
    comments = Comment.objects.filter(product_id=product.id).order_by('-id')
    form = CartAddForm()

    is_favourite = False
    if product.favourite.filter(id=request.user.id).exists():
        is_favourite = True

    if request.method == 'POST':
        variant = Variants.objects.filter(product__slug=product_slug)
        var_id = request.POST.get('select')
        variants = Variants.objects.get(id=var_id)
        sizes = Variants.objects.filter(
            product_id=product.id,
            color_variant_id=variants.color_variant_id
        )
        colors = Variants.objects.filter(product__slug=product_slug).distinct('color_variant_id')
    else:
        variant = Variants.objects.filter(product__slug=product_slug)
        variants = Variants.objects.get(id=variant[0].id)
        sizes = Variants.objects.filter(
            product_id=product.id,
            color_variant_id=variants.color_variant_id
        )
        colors = Variants.objects.filter(product__slug=product_slug).distinct('color_variant_id')
    context = {
        'product': product,
        'comment_form': comment_form,
        'comments': comments,
        'product_images': product_images,
        'form': form,
        'variant': variant,
        'variants': variants,
        'colors': colors,
        'sizes': sizes,
        'compare': Compare.objects.filter(product_id=product.id),
        'is_favourite': is_favourite,
        'related_products': Product.objects.get_queryset().filter(is_available=True,
                                                                  category__products=product).exclude(
            id=product.id).distinct()[:8],
    }
    return render(request, 'store/product_detail.html', context)


@login_required
def product_comment(request, productId):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            Comment.objects.create(user_id=request.user.id, product_id=productId, title=data['title'],
                                   text=data['text'], rate=data['rate'], is_recommended=data['is_recommended'])
        return redirect(url)


@login_required
def comment_like(request, commentId):
    url = request.META.get('HTTP_REFERER')
    comment = Comment.objects.get(id=commentId)
    if comment.comment_like.filter(id=request.user.id).exists():
        comment.comment_like.remove(request.user)
        messages.success(request, 'لایک شما حذف شد.')
    else:
        comment.comment_like.add(request.user)
        messages.success(request, 'لایک شما ثبت شد.')

    return redirect(url)


@login_required
def comment_dislike(request, commentId):
    url = request.META.get('HTTP_REFERER')
    comment = Comment.objects.get(id=commentId)
    if comment.comment_dislike.filter(id=request.user.id).exists():
        comment.comment_dislike.remove(request.user)
        messages.success(request, 'لایک شما حذف شد.')
    else:
        comment.comment_dislike.add(request.user)
        messages.success(request, 'لایک شما ثبت شد.')

    return redirect(url)


def category_list(request, category_slug):
    products = Product.objects.filter(category__slug=category_slug)
    products_filter = ProductFilter(request.GET, queryset=products)
    products = products_filter.qs

    # page
    paginator = Paginator(products, 1)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    data = request.GET.copy()
    if 'page' in data:
        del data['page']

    # category
    category = get_object_or_404(Category, slug=category_slug)

    context = {
        'products': products,
        'products_filter': products_filter,
        'page_obj': page_obj,
        'page_num': page_num,
        'category': category,
        'data': urlencode(data),
    }
    return render(request, 'store/category_list.html', context)


def tag_list(request, tag_slug):
    products = Product.objects.filter(tag__slug=tag_slug)

    # page
    paginator = Paginator(products, 1)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    # category
    tag = get_object_or_404(Tag, slug=tag_slug)

    context = {
        'products': products,
        'page_obj': page_obj,
        'page_num': page_num,
        'tag': tag
    }
    return render(request, 'store/tag_list.html', context)


def brand_list(request, brand_slug):
    products = Product.objects.filter(brand__slug=brand_slug)

    # page
    paginator = Paginator(products, 1)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    # category
    brand = get_object_or_404(Brand, slug=brand_slug)

    context = {
        'products': products,
        'page_obj': page_obj,
        'page_num': page_num,
        'brand': brand
    }
    return render(request, 'store/brand_list.html', context)


class SearchListView(ListView):
    template_name = 'store/search.html'
    paginate_by = 1

    def get_queryset(self):
        search = self.request.GET.get('q')
        return Product.objects.filter(
            Q(title__icontains=search) | Q(english_title__icontains=search) | Q(slug__icontains=search))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search': self.request.GET.get('q'),
        })
        return context

@login_required
def favourite_product(request, productSlug):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(slug=productSlug)
    is_favourite = False
    if product.favourite.filter(id=request.user.id).exists():
        product.favourite.remove(request.user)
        is_favourite = False
        messages.warning(request, f'محصول {product.title} از لیست علاقه مندی شما حذف شد.')
    else:
        product.favourite.add(request.user)
        is_favourite = True
        messages.success(request, f'محصول {product.title} به لیست علاقه مندی شما اضافه شد.')
    return redirect(url)
