from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.carts.models import Cart
from apps.general.models import General,PaymentMethod


@login_required
def checkout(request):
    carts = Cart.objects.filter(user=request.user).select_related('product')
    if not carts:
        return redirect('carts:cart')
    try:
        shipping_percent = General.objects.first().shipping_percent
    except AttributeError:
        shipping_percent = 0

    coupon_discount_percent = request.session.get('coupon_data', {}).get('discount_percent', 0)

    total_cart = sum([cart.quantity * cart.product.price for cart in carts])
    total_sum = total_cart + total_cart * shipping_percent / 100 - total_cart * coupon_discount_percent / 100

    payment_methods = PaymentMethod.objects.order_by('name')

    context ={
        'carts':carts,
        'page': 'pages',
        'total_cart': total_cart,
        'shipping_percent': shipping_percent,
        'total_sum':total_sum,
        'payment_methods':payment_methods

    }


    return render(
        request=request,
        template_name='checkout.html',
        context=context
    )

@login_required
def cert_order(request):
    return redirect('home-page')