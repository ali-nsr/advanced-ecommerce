from django.db import models
from store.models import Product


class CompareTitle(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان مقایسه')
    title_admin = models.CharField(max_length=100, verbose_name='عنوان مقایسه برای نمایش در ادمین')

    def __str__(self):
        return self.title_admin

    class Meta:
        verbose_name = 'عنوان مقایسه'
        verbose_name_plural = 'عنوان های مقایسه'


class CompareSpecifications(models.Model):
    title_1 = models.CharField(max_length=100, verbose_name='عنوان اول')
    title_2 = models.CharField(max_length=100, verbose_name='عنوان دوم')
    compare_title = models.ForeignKey(CompareTitle, on_delete=models.CASCADE, related_name='compare_specifications',
                                      verbose_name='عنوان مقایسه')

    class Meta:
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی ها محصول'


class Compare(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_compares',
                                verbose_name='محصول')
    title = models.ForeignKey(CompareTitle, on_delete=models.CASCADE, related_name='title_compares',
                              verbose_name='عنوان')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'مقایسه'
        verbose_name_plural = 'مقایسه ها'
