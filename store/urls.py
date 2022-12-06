from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.home, name='home_page'),
    path('product/<product_slug>', views.product_detail, name='product_detail_page'),
    path('comment/<productId>', views.product_comment, name='product_comment'),
    path('like_comment/<commentId>', views.comment_like, name='comment_like'),
    path('dislike_comment/<commentId>', views.comment_dislike, name='comment_dislike'),
    path('category/<category_slug>', views.category_list, name='category_list'),
    path('tag/<tag_slug>', views.tag_list, name='tag_list'),
    path('brand/<brand_slug>', views.brand_list, name='brand_list'),
    path('search/', views.SearchListView.as_view(), name='search'),
    # favourite products
    path('favourite/<productSlug>', views.favourite_product, name='favourite_product'),
]
