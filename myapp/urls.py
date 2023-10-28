from django.urls import path

from .views import DateOrders, create_product
from myapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('orders_products/<int:client_id>/<int:days>', DateOrders.as_view(), name='month_post'),
    path('create_product/', create_product, name='create_product'),
]