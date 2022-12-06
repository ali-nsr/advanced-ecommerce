from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from blog.models import Article
from store.models import Product


# class StaticViewSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.5
#
#     def items(self):
#         return ['site_setting:about_us', 'site_setting:faq',
#                 'site_setting:privacy_policy',
#                 'site_setting:rules', 'contact_us:contact_us_page']
#
#     def location(self, item):
#         return reverse(item)


class HomesViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ['store:home_page']

    def location(self, item):
        return reverse(item)


class ProductViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Product.objects.get_published_products()

    def lastmod(self, item):
        return item.updated_date


class ArticleViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Article.objects.get_active_articles()

    def lastmod(self, item):
        return item.updated_date
