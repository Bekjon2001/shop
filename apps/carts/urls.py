from django.urls import path
from apps.carts.views import CartsViews, CartCreateView,CartDeleteView,SetCarQuantityView

app_name = 'carts'
urlpatterns = [
    path("", CartsViews.as_view(), name="cart"),
    path("create/<int:product_id>/", CartsViews.as_view(), name="cart_create"),
    path("delete/<int:product_id>/",CartDeleteView.as_view(), name="delete_cart"),
    path("set/<int:cart_id>/", SetCarQuantityView.as_view(), name="set-cart_quantity"),
]