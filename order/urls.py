from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('order-paid/<order_id>', views.order_is_paid, name='order_is_paid'),
    path('order-form', views.order_form, name='order_form'),
    path('order-create/', views.order_create, name='order_create'),
    path('order-complete/<order_id>/', views.order_complete, name='order_complete'),

    path('ajax/load-cities', views.load_cities, name='load_cities'),  # ajax load cities

    path('request/<pk>/<price>/', views.send_request_payment, name='request_payment'),
    path('verify/', views.verify, name='verify'),
]
