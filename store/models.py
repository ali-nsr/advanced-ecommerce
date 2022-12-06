from django.db import models
from django.utils.html import format_html
from django.shortcuts import reverse
from services.utils import *
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Avg
from accounts.models import User


class CategoryManager(models.Manager):
    def get_published_categories(self):
        return self.filter(status=True)


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.CASCADE,
                               related_name='children', verbose_name='زیر دسته')
    title = models.CharField(max_length=255, verbose_name='عنوان')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='آدرس URL دسته بندی')
    status = models.BooleanField(default=True, verbose_name='انتشار')
    position = models.IntegerField(verbose_name='موقعیت')
    image = models.ImageField(upload_to='category', null=True, blank=True, verbose_name='تصویر دسته بندی')
    meta_description = models.TextField(max_length=300, verbose_name='توضیحات متای صفحه دسته بندی')
    meta_keywords = models.TextField(max_length=300, verbose_name='کلمه های کلیدی صفحه دسته بندی')

    objects = CategoryManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['parent__id', 'position']

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])


class Tag(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان')
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, verbose_name='آدرس URL')
    meta_description = models.TextField(max_length=300, verbose_name='توضیحات متای صفحه تگ')
    meta_keywords = models.TextField(max_length=300, verbose_name='کلمه های کلیدی صفحه تگ')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ ها'

    def get_absolute_url(self):
        return reverse('store:tag_list', args=[self.slug])


class Brand(models.Model):
    title = models.CharField(max_length=100, verbose_name='برند')
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, verbose_name='آدرس url')
    meta_description = models.TextField(max_length=300, verbose_name='توضیحات متای صفحه برند')
    meta_keywords = models.TextField(max_length=300, verbose_name='کلمه های کلیدی صفحه برند')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('store:brand_list', args=[self.slug])


class ProductManager(models.Manager):
    def get_published_products(self):
        return self.filter(is_published=True)

    def get_gaming_consoles(self):
        return self.filter(status='gaming_consoles', is_published=True)


class Position(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='عنوان')
    image = models.ImageField(upload_to='images', verbose_name='تصویر')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'محل قرار گیری محصول'
        verbose_name_plural = 'محل های قرار گیری محصولات'


class Product(models.Model):
    SC_CHOICES = (
        ('None', 'ندارد'),
        ('size', 'سایز'),
        ('color', 'رنگ'),
        ('both', 'سایز و رنگ'),
    )
    title = models.CharField(max_length=255, verbose_name='عنوان')
    english_title = models.CharField(max_length=255, verbose_name='عنوان به انگلیسی')
    window_title = models.CharField(max_length=255, verbose_name='عنوان در مرورگر')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='آدرس URL')
    category = models.ManyToManyField(Category, related_name='products', verbose_name='دسته بندی')
    tag = models.ManyToManyField(Tag, related_name='products', verbose_name='تگ')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_products', verbose_name='برند')
    weight = models.PositiveIntegerField(verbose_name='وزن به گرم')
    unit_price = models.PositiveBigIntegerField(verbose_name='قیمت واحد')
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name='تخفیف')
    total_price = models.PositiveIntegerField(verbose_name='قیمت نهایی')
    description = RichTextUploadingField(verbose_name='توضیحات')
    image = models.ImageField(upload_to='product', verbose_name='تصویر اصلی')
    image_alt = models.CharField(max_length=255, verbose_name='متن جایگزین تصویر اصلی')
    is_available = models.BooleanField(default=True, verbose_name='فعال / غیر فعال')
    is_published = models.BooleanField(default=True, verbose_name='منتشر شده / نشده')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='positions',
                                 verbose_name='محل قرار گیری')
    size_and_color = models.CharField(max_length=100, choices=SC_CHOICES, default='None', verbose_name='سایز و رنگ')
    sell = models.PositiveIntegerField(default=0)
    favourite = models.ManyToManyField(User, blank=True, related_name='favourites_user')
    meta_description = models.TextField(max_length=300, verbose_name='توضیحات متای محصول')
    meta_keywords = models.TextField(max_length=300, verbose_name='کلمه های کلیدی محصول')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    def __str__(self):
        return f'{self.title} | {self.slug}'

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def jalali_created_date(self):
        return jalali_converter(self.created_date)

    jalali_created_date.short_description = 'تاریخ انتشار'

    def jalali_updated_date(self):
        return jalali_converter(self.updated_date)

    jalali_updated_date.short_description = 'تاریخ آپدیت'

    jalali_created_date.short_description = 'تاریخ انتشار'

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price

    total_price.fget.short_description = 'قیمت نهایی'

    def avg_review(self):
        reviews = Comment.objects.filter(product=self).aggregate(mean=Avg('rate'))
        avg = 0
        if reviews['mean'] is not None:
            avg = float(reviews['mean'])
        return avg

    def image_tag(self):
        return format_html('<img width=100 height=100 style="border-radius: 10px;" src="{}">'.format(self.image.url))

    image_tag.short_description = 'تصویر'

    def get_absolute_url(self):
        return reverse('store:product_detail_page', args=[self.slug])


class Size(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    price = models.PositiveBigIntegerField(default=0, verbose_name='قیمت')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'سایز'
        verbose_name_plural = 'سایز ها'


class Color(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    price = models.PositiveBigIntegerField(default=0, verbose_name='قیمت')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ ها'


class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name='عنوان')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variant', blank=True,
                                null=True, verbose_name='محصول')
    size_variant = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name='سایز')
    color_variant = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name='رنگ')
    v_amount = models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد موجود')
    unit_price = models.PositiveBigIntegerField(blank=True, null=True, verbose_name='قیمت واحد')
    discount_variant = models.IntegerField(default=0, blank=True, null=True, verbose_name='تخفیف')
    total_price = models.IntegerField(blank=True, null=True, verbose_name='قیمت نهایی')

    def __str__(self):
        try:
            return f'{self.title} {self.size_variant.title} {self.color_variant.title}'
        except:
            return self.title

    class Meta:
        verbose_name = 'انواع محصولات'
        verbose_name_plural = 'نوع محصول'

    @property
    def total_price(self):
        if self.product.size_and_color == 'both':
            if not self.discount_variant:
                return self.unit_price + self.size_variant.price + self.color_variant.price
            else:
                total = (self.unit_price * self.discount_variant) / 100
                return int((self.unit_price + self.size_variant.price + self.color_variant.price) - total)

        elif self.product.size_and_color == 'size':
            if not self.discount_variant:
                return self.unit_price + self.size_variant.price
            else:
                total = (self.unit_price * self.discount_variant) / 100
                return int((self.unit_price + self.size_variant.price) - total)

        elif self.product.size_and_color == 'color':
            if not self.discount_variant:
                return self.unit_price + self.color_variant.price
            else:
                total = (self.unit_price * self.discount_variant) / 100
                return int((self.unit_price + self.color_variant.price) - total)

        elif self.product.size_and_color == 'None':
            if not self.discount_variant:
                return self.unit_price
            else:
                total = (self.unit_price * self.discount_variant) / 100
                return int(self.unit_price - total)

        return self.total_price

    def total_price_without_gte(self):
        if not self.discount_variant:
            return self.unit_price
        else:
            total = (self.unit_price * self.discount_variant) / 100
            return int(self.unit_price - total)


class Comment(models.Model):
    COMMENT_STATUS_CHOICES = (
        ('need_approve', 'در انتظار تایید'),
        ('approved', 'تایید شده'),
        ('not_approved', 'تایید نشده'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='محصول')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    text = models.TextField(verbose_name='کامنت')
    rate = models.PositiveIntegerField(default=1, verbose_name='امتیاز به محصول')
    is_recommended = models.BooleanField(default=True, verbose_name='توصیه به خرید')
    comment_like = models.ManyToManyField(User, blank=True, related_name='com_like', verbose_name='لایک کامنت')
    comment_dislike = models.ManyToManyField(User, blank=True, related_name='com_dislike', verbose_name='دیسلایک کامنت')
    status = models.CharField(max_length=20, choices=COMMENT_STATUS_CHOICES, default='need_approve',
                              verbose_name='وضعیت')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def jalali_created_date(self):
        return jalali_converter(self.created_date)

    jalali_created_date.short_description = 'تاریخ ثبت'

    def total_likes(self):
        return self.comment_like.count()

    def total_dislikes(self):
        return self.comment_dislike.count()


class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    title = models.CharField(max_length=255, verbose_name='عنوان')
    image = models.ImageField(upload_to='images', verbose_name='تصویر')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'عکس'
        verbose_name_plural = 'گالری محصولات'

    def image_tag(self):
        return format_html('<img width=100 height=100 style="border-radius: 10px;" src="{}">'.format(self.image.url))

    image_tag.short_description = 'تصویر'


class Specifications(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_specifications',
                                verbose_name='محصول')
    title = models.CharField(max_length=150, blank=True, null=True, verbose_name='عنوان')
    characteristic = models.CharField(max_length=150, blank=True, null=True, verbose_name='مشخصه')

    class Meta:
        verbose_name = 'مشخصه محصول'
        verbose_name_plural = 'مشخصات محصول'

    def __str__(self):
        if self.title:
            return self.title
        else:
            return '---'
