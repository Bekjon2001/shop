from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from apps.carts.models import Cart


def cart(request: WSGIRequest):
    context = {
        'cart': Cart.objects.filter(user=request.user).select_related('product')
    }
    return render(request=request, template_name='cart.html', context=context)


@login_required(login_url='login-page')
def cart_create(request: WSGIRequest, product_id: int):
    quantity = request.POST.get('cart_quantity', 1)
    obj, create = Cart.objects.get_or_create(product_id=product_id, user=request.user)
    if obj.quantity != quantity:
        obj.quantity = quantity
        obj.save()

    return redirect(request.META['HTTP_REFERER'])


def delete_cart(request: WSGIRequest, product_id: int) -> None:
    print(f"Deleting product with ID: {product_id}")
    if product_id:
        Cart.objects.filter(product_id=product_id).delete()
    return redirect('carts:cart')
