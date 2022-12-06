from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from services.sitemaps import *

sitemaps = {
    'homes': HomesViewSitemap,
    'product': ProductViewSitemap,
    'article': ArticleViewSitemap,
}

urlpatterns = [
    path('', include('store.urls', namespace='store')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('account/', include('accounts.urls', namespace='accounts')),
    path('order/', include('order.urls', namespace='order')),
    path('', include('ticket.urls', namespace='ticket')),
    path('', include('blog.urls', namespace='blog')),
    path('', include('compare.urls', namespace='compare')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
