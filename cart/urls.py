from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add-to-cart', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<variant_id>', views.remove_from_cart, name='remove_from_cart'),
]
