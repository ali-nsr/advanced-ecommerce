from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('mag', views.BlogHome.as_view(), name='blog_home'),
    path('mag/<article_slug>', views.blog_detail, name='blog_detail'),
    path('mag/category/<categorySlug>', views.BlogCategoryListView.as_view(), name='blog_category_list'),
    path('mag/tag/<tagSlug>', views.BlogTagListView.as_view(), name='blog_tag_list'),
    path('mag/search/', views.BlogSearchListView.as_view(), name='blog_search_list'),
    path('mag/add-commet/<articleId>', views.add_blog_comment, name='add_blog_comment'),
    path('mag/add-article-comment-reply/<int:articleId>/<int:commentId>', views.add_blog_comment_reply,
         name='add_blog_comment_reply'),
]
