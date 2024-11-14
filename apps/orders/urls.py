from django.urls import path

from apps.orders.views import checkout,cert_order

urlpatterns=[
    path('',checkout,name='checkout-page'),
    path('create-order/',cert_order,name='create-order')
]