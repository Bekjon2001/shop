from django.urls import path

from apps.products.views import product_list, ProductDetailView, product_by_feature

app_name = 'products'
urlpatterns = [
    path('', product_list, name='product_list'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail-page'),
    path('detail/feature/<int:pk>/', product_by_feature, name='product_by_feature'),
]
