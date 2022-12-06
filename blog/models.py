from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()


class BlogCategory(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True,
                               verbose_name='زیر دسته')
    name = models.CharField(max_length=200, verbose_name='نام دسته بندی')
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, verbose_name='آدرس url')
    blog_category_meta_description = models.TextField(max_length=200, blank=True, null=True,
                                                      verbose_name='توضیحات متا')
    blog_category_meta_keywords = models.TextField(max_length=200, blank=True, null=True,
                                                   verbose_name='کلمه های کلیدی')
    status = models.BooleanField(default=True, verbose_name='نمایش / عدم نمایش')
    meta_description = models.TextField(max_length=300, verbose_name='توضیحات متای صفحه دسته بندی')
    meta_keywords = models.TextField(max_length=300, verbose_name='کلمه های کلیدی صفحه دسته بندی')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:blog_category_list', args=[self.slug])


class BlogTag(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name='عنوان')
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, verbose_name='آدرس url')
    status = models.BooleanField(default=True, verbose_name='نمایش / عدم نمایش')
    meta_description = models.TextField(max_length=300, verbose_name='توضیحات متای صفحه تگ')
    meta_keywords = models.TextField(max_length=300, verbose_name='کلمه های کلیدی صفحه تگ')

    class Meta:
        verbose_name = 'تگ / برچسب'
        verbose_name_plural = 'تگ ها / برچسب ها'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_tag_list', args=[self.slug])


class ArticleManager(models.Manager):
    def get_active_articles(self):
        return self.filter(is_active=True)


class Article(models.Model):
    STATUS = (
        ('article', 'مقاله'),
        ('news', 'خبر'),
        ('video', 'فیلم'),
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='نویسنده')
    title = models.CharField(max_length=250, verbose_name='عنوان مقاله')
    article_browser_title = models.CharField(max_length=60, unique=True,
                                             verbose_name='آدرس سایت در مرورگر')
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, verbose_name='آدرس url')
    image = models.ImageField(upload_to='images/blog-header/', verbose_name='تصویر شاخص')
    image_alt = models.CharField(max_length=200, verbose_name='متن جایگزین تصویر')
    categories = models.ManyToManyField(BlogCategory, related_name='article', blank=True, verbose_name='دسته بندی')
    tags = models.ManyToManyField(BlogTag, related_name='article', blank=True, verbose_name='تگ / برچسب')
    status = models.CharField(max_length=10, choices=STATUS, default='article', verbose_name='نوع محتوا')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    content = RichTextUploadingField(verbose_name='توضیحات مقاله')
    # article_hits = models.ManyToManyField(User, blank=True, related_name='article_hits',
    #                                       verbose_name='افرادی که از این محتوا بازدید کرده اند')
    # article_num_hits = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')
    has_video = models.BooleanField(default=False, verbose_name='شامل کلیپ است')
    meta_description = models.TextField(max_length=300, verbose_name='توضیحات متای صفحه مقاله')
    meta_keywords = models.TextField(max_length=300, verbose_name='کلمه های کلیدی صفحه مقاله')
    article_robots = models.CharField(max_length=100, default='index,follow', blank=True, null=True,
                                      verbose_name='تگ robots')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    objects = ArticleManager()

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=[self.slug])


class BlogComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_blog_comments', verbose_name='کاربر')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='blog_comments',
                                verbose_name='محتوا')
    content = models.TextField(verbose_name='کامنت')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_blog_comments', null=True,
                              blank=True,
                              verbose_name='پاسخ به کامنت')
    # reply_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_reply_to', blank=True,
    #                              null=True, verbose_name='در پاسخ به')
    is_reply = models.BooleanField(default=False, verbose_name='آیا پاسخ دارد؟')
    is_published = models.BooleanField(default=True, verbose_name='وضعیت انتشار')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'
