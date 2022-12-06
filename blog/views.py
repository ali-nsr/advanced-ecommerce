from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q
from .models import *
from .forms import *
from site_seo.models import BlogSeo
from django.contrib.auth.decorators import login_required


class BlogHome(ListView):
    template_name = 'blog/blog_home.html'
    paginate_by = 32

    def get_queryset(self):
        return Article.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super(BlogHome, self).get_context_data(**kwargs)
        context['blog_home_seo'] = BlogSeo.objects.first()
        return context


def blog_detail(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug)
    comments = BlogComment.objects.filter(article_id=article.id, is_reply=False).order_by('-created_date')
    reply_comments = BlogComment.objects.filter(article_id=article.id, is_reply=True).order_by('-created_date')
    comments_count = comments.count() + reply_comments.count()
    context = {
        'article': article,
        'comments': comments,
        'comments_count': comments_count,
    }
    return render(request, 'blog/blog_detail.html', context)


@login_required
def add_blog_comment(request, articleId):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            BlogComment.objects.create(user_id=request.user.id, article_id=articleId, content=data['content'])
            messages.success(request,
                             'کامنت شما با موفقیت ثبت شد')
        return redirect(url)


@login_required
def add_blog_comment_reply(request, articleId, commentId):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CourseCommentReplyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            BlogComment.objects.create(user_id=request.user.id, article_id=articleId, content=data['content'],
                                       reply_id=commentId, is_reply=True,
                                       is_published=True)
            messages.success(request,
                             'پاسخ شما با موفقیت ثبت شد')
        return redirect(url)


class BlogCategoryListView(ListView):
    template_name = 'blog/blog_category_list.html'
    paginate_by = 16

    def get_queryset(self):
        global category
        slug = self.kwargs.get('categorySlug')
        category = get_object_or_404(BlogCategory, slug=slug)
        return category.article.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        context['articles'] = Article.objects.get_active_articles().order_by('-created_date')[:]
        return context


class BlogTagListView(ListView):
    template_name = 'blog/blog_tag_list.html'
    paginate_by = 16

    def get_queryset(self):
        global tag
        slug = self.kwargs.get('tagSlug')
        tag = get_object_or_404(BlogTag, slug=slug)
        return tag.article.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = tag
        context['articles'] = Article.objects.get_active_articles().order_by('-created_date')[:]
        return context


class BlogSearchListView(ListView):
    template_name = 'blog/blog_search_list.html'
    paginate_by = 16

    def get_queryset(self):
        name = self.request.GET.get('mq')
        return Article.objects.filter(Q(title__icontains=name) | Q(slug__icontains=name))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('mq')
        context['articles'] = Article.objects.get_active_articles()
        return context
