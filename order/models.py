from django.db import models
from accounts.models import User
from store.models import Product, Variants
from services.utils import jalali_converter
from shipping.models import Provinces, Cities


class Order(models.Model):
    STATUS_CHOICES = (
        ('P', 'پرداخت شده'),
        ('S', 'در حال ارسال'),
        ('R', 'تحویل داده شده'),
        ('N', 'پرداخت نشده'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    order_code = models.CharField(max_length=20, unique=True, editable=False, verbose_name='کد پیگیری')
    first_name = models.CharField(max_length=100, verbose_name='نام')
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    phone = models.CharField(max_length=11, verbose_name='شماره همراه')
    province = models.ForeignKey(Provinces, on_delete=models.CASCADE, verbose_name='استان')
    city = models.ForeignKey(Cities, on_delete=models.CASCADE, verbose_name='شهر')
    address = models.CharField(max_length=250, verbose_name='آدرس')
    discount = models.PositiveIntegerField(null=True, blank=True, verbose_name='تخفیف')
    total = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='قیمت نهایی')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت')
    admin_note = models.CharField(max_length=150, blank=True, verbose_name='یادداشت مدیر')
    order_description = models.TextField(max_length=500, blank=True, verbose_name='توضیحات سفارش')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='وضعیت سفارش')
    shipping_price = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='هزینه حمل و نقل')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ سفارش')

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'

    def jalali_created_date(self):
        return jalali_converter(self.created_date)

    jalali_created_date.short_description = 'تاریخ سفارش'

    @property
    def total(self):
        total = sum(item.get_price() for item in self.item_orders.all())
        total += self.shipping_price
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total

    def get_day_total(self):
        day_total = sum(item.get_day_price() for item in self.item_orders.all())
        day_total += self.shipping_price
        if self.discount:
            discount_price = (self.discount / 100) * day_total
            return int(day_total - discount_price) * 10
        return day_total * 10

    def get_day_total_for_user(self):
        day_total = sum(item.get_day_price() for item in self.item_orders.all())
        day_total += self.shipping_price
        if self.discount:
            discount_price = (self.discount / 100) * day_total
            return int(day_total - discount_price)
        return day_total

    def number(self):
        return f'HG-{self.user.id}-{self.id}'

    number.short_description = 'شماره سفارش'


class ItemOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='item_orders',
                              verbose_name='سفارش')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    variant = models.ForeignKey(Variants, null=True, blank=True, on_delete=models.CASCADE, verbose_name='نوع محصول')
    console_guarantee = models.CharField(max_length=200, null=True, blank=True, verbose_name='گارانتی کنسول')
    controller_guarantee = models.CharField(max_length=200, null=True, blank=True, verbose_name='گارانتی دسته')
    unit_price = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='قیمت واحد بدون تخفیف')
    unit_price_with_discount = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='قیمت واحد با تخیف')
    discount = models.IntegerField(null=True, blank=True, verbose_name='تخفیف')
    quantity = models.IntegerField(null=True, blank=True, verbose_name='تعداد')
    price = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='قیمت تمام شده')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ سفارش')

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'جزییات سفارش'
        verbose_name_plural = 'جزییات سفارش ها'

    def jalali_created_date(self):
        return jalali_converter(self.created_date)

    jalali_created_date.short_description = 'تاریخ سفارش'

    def get_price(self):
        return self.price * self.quantity

    def get_total(self):
        return self.order.total

    def get_day_price(self):
        return self.variant.total_price * self.quantity

    @property
    def title(self):
        return self.variant.product_variant.title

    title.fget.short_description = 'نام محصول'

    def unit_price_discount(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.unit_price * self.discount) / 100
            return int(self.unit_price - total)

    unit_price_discount.short_description = 'قیمت واحد با تخفیف'

    def sub_total(self):
        if self.price and self.quantity:
            sub_total = int(self.price * self.quantity)
            return sub_total
        else:
            return None

    sub_total.short_description = 'قیمت تمام شده'
