from django.urls import path
from .views import cart, cart_create,delete_cart

app_name = 'cart'
urlpatterns = [
    path("", cart, name="cart"),
    path("create/<int:product_id>/", cart_create, name="cart_create"),
    path("delete/<int:product_id>/", delete_cart, name="delete_cart"),
]