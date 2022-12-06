from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager
from django.core.validators import RegexValidator
from services.utils import jalali_converter

# regex phone number
phone_number_validation = RegexValidator(
    regex=r'^[0][9]\d{9}$',
    message='لطفا یک شماره همراه معتبر وارد کنید.'
)


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=250, verbose_name='نام')
    last_name = models.CharField(max_length=250, verbose_name='نام خانوادگی')
    email = models.EmailField(max_length=250, unique=True, verbose_name='ایمیل')
    image = models.ImageField(upload_to='user-images', null=True, blank=True, verbose_name='تصویر کاربر')
    province = models.CharField(max_length=100, null=True, blank=True, verbose_name='استان')
    city = models.CharField(max_length=150, null=True, blank=True, verbose_name='شهر')
    phone = models.CharField(max_length=11, validators=[phone_number_validation],
                             unique=True,
                             verbose_name='شماره تلفن')
    post_code = models.CharField(max_length=12, null=True, blank=True, verbose_name='کد پستی')
    address = models.CharField(max_length=300, null=True, blank=True, verbose_name='آدرس')
    is_superuser = models.BooleanField(default=False, verbose_name='مدیر')
    is_news_letter = models.BooleanField(default=False, verbose_name='عضویت در خبرنامه')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیر فعال')
    is_verify = models.BooleanField(default=False, verbose_name='تایید شده / نشده')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')
    is_editor = models.BooleanField(default=False, verbose_name='نویسنده ارشد')
    has_setting_access = models.BooleanField(default=False, verbose_name='دسترسی به تنظیمات')
    is_writer = models.BooleanField(default=False, verbose_name='نویسنده')
    temp_code = models.CharField(max_length=255, null=True, blank=True, verbose_name='کد موقت')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ عضویت')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    # fields required for admin
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def jalali_created_date(self):
        return jalali_converter(self.created_date)

    jalali_created_date.short_description = 'تاریخ انتشار'

    def has_perm(self, perm, obj=None):
        # if self.is_superuser:
        return True

    def has_module_perms(self, app_label):
        return True
        # if app_label == 'users_account':
        #     if self.is_superuser:
        #         return True
        # elif app_label == 'store':
        #     if self.is_superuser or self.is_admin:
        #         return True
        # elif app_label == 'order':
        #     if self.is_superuser or self.is_admin:
        #         return True
        # elif app_label == 'slider':
        #     if self.is_superuser or self.is_admin:
        #         return True
        # elif app_label == 'site_setting':
        #     if self.is_superuser or self.is_admin:
        #         return True
        # elif app_label == 'blog':
        #     if self.is_superuser or self.is_admin or self.is_writer or self.is_editor:
        #         return True

    @property
    def is_staff(self):
        if self.is_superuser:
            return True
        elif self.is_admin:
            return True
        elif self.is_writer:
            return True
        elif self.is_editor:
            return True

    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.email

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
