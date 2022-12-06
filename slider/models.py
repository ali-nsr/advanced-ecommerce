from django.db import models
from store.models import Product
from django.utils.html import format_html


class SliderHomeManager(models.Manager):
    def get_published_sliders(self):
        return self.filter(status=True)


class SliderHome(models.Model):
    image = models.ImageField(upload_to='images/slider', verbose_name='تصویر اسلایدر')
    image_title = models.CharField(max_length=255, verbose_name='عنوان تصویر')
    image_alt = models.CharField(max_length=255, verbose_name='متن جایگزین تصویر')
    url = models.URLField(verbose_name='آدرس URL')
    status = models.BooleanField(default=False, verbose_name='وضعیت انتشار')

    objects = SliderHomeManager()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'اسلایدر فروشگاه'
        verbose_name_plural = 'اسلایدر های فروشگاه'

    def image_tag(self):
        return format_html('<img width=100 height=100 style="border-radius: 10px;" src="{}">'.format(self.image.url))

    image_tag.short_description = 'تصویر'


class SliderHomeOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'اسلایدر تخفیف فروشگاه'
        verbose_name_plural = 'اسلایدر های تخفیف فروشگاه'


class SliderOfferDate(models.Model):
    when = models.DateTimeField(verbose_name='تاریخ تخفیف')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'تاریخ تخفیف فروشگاه'
        verbose_name_plural = 'تاریخ های تخفیف فروشگاه'


class BlogSlider(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    image = models.ImageField(upload_to='images/slider', verbose_name='تصویر')
    url_address = models.URLField(verbose_name='آدرس URL')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'اسلایدر مجله'
        verbose_name_plural = 'اسلایدر های مجله'
