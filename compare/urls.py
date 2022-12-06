from django.urls import path
from . import views

app_name = 'compare'
urlpatterns = [
    path('compare', views.compare, name='compare_page'),
    path('compare/add/<product_slug>', views.add_compare, name='add_compare'),
    path('compare/remove/<product_slug>', views.remove_compare, name='remove_compare'),
]