from django.db import models
from django.contrib.auth import get_user_model
from services.utils import jalali_converter, jalali_converter_detail

User = get_user_model()


class Ticket(models.Model):
    STATUS = (
        ('open', 'باز'),
        ('close', 'بسته'),
    )
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='user_ticket',
                             verbose_name='کاربر')
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name='عنوان')
    status = models.CharField(default='open', max_length=10, choices=STATUS, verbose_name='وضعیت تیکت')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    def jalali_created_date(self):
        return jalali_converter_detail(self.created_date)
    jalali_created_date.short_description = 'تاریخ ثبت تیکت'


class TicketUser(models.Model):
    from django.utils.timezone import now
    STATUS_CHOICES = (
        ('in_progress', 'در حال بررسی'),
        ('answered', 'پاسخ داده شده'),
        ('not_received', 'ارسال شده'),
    )
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name='عنوان')
    ticket = models.ForeignKey('Ticket', null=True, blank=True, on_delete=models.CASCADE,
                               related_name='ticket_ticketUser', verbose_name='تیکت')
    content = models.TextField(null=True, blank=True, verbose_name='متن تیکت کاربر')
    reply = models.TextField(null=True, blank=True, verbose_name='متن پاسخ ادمین')
    ticketUserStatus = models.CharField(default='not_received', max_length=20, choices=STATUS_CHOICES,
                                        verbose_name='وضعیت این تیکت')
    content_created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال تیکت')
    reply_created_date = models.DateTimeField(default=now, blank=True, verbose_name='تاریخ ارسال تیکت')

    def __str__(self):
        if not self.title:
            return 'پاسخ'
        return self.ticket.user.email

    class Meta:
        verbose_name = 'جزییات تیکت'
        verbose_name_plural = 'جزییات تیکت ها'

    def jalali_created_date(self):
        return jalali_converter_detail(self.content_created_date)
    jalali_created_date.short_description = 'تاریخ ثبت'

    def jalali_reply_date(self):
        return jalali_converter_detail(self.reply_created_date)
