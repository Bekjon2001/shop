from django.urls import path

from apps.orders.views import checkout,create_order

urlpatterns=[
    path('',checkout,name='checkout-page'),
    path('create-order/',create_order,name='create-order')
]