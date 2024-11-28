
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Sum
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from apps.carts.models import Cart
from apps.general.models import General


class CartsViews(LoginRequiredMixin,View):
    def get (self, request: WSGIRequest):
        try:
            shipping_percent = General.objects.first().shipping_percent
        except AttributeError:
            shipping_percent = 0
        quryset = Cart.objects.annotate(total_price=F('quantity') * F('product__price')).filter(user=request.user)
        context = {
            'cart': quryset.select_related('product'),
            'cart_total_price': quryset.aggregate(Sum('total_price'))['total_price__sum'],
            'shipping_percent': shipping_percent
        }
        if not context['cart_total_price'] == None:
            context['total_price'] = context['cart_total_price'] + context['cart_total_price'] * shipping_percent / 100 - context['cart_total_price'] * request.session.get('coupon_data', {}).get('discount_percent', 0) / 100


        return render(request=request, template_name='cart.html', context=context)

class CartCreateView(LoginRequiredMixin,View):
    def post(self,request: WSGIRequest, product_id: int):
        user = request.user
        quantity = request.POST.get('cart_quantity', 1)
        obj, create = Cart.objects.get_or_create(product_id=product_id, user=user)
        if obj.quantity != quantity:
            obj.quantity = quantity
            obj.save()

        return redirect(request.META['HTTP_REFERER','/'])

class CartDeleteView(View):
    def get(self,request: WSGIRequest, product_id: int) -> None:
        Cart.objects.filter(product_id=product_id).delete()
        return redirect(request.META['HTTP_REFERER'])


class SetCarQuantityView(View):
    def post(self,request, cart_id):
        cart_obj = get_object_or_404(Cart, pk=cart_id)
        quantity = request.POST.get('item_quantity', cart_obj.quantity)
        if quantity.isdigit() and int(quantity) <= 0:
            quantity = 0
        cart_obj.quantity = quantity
        cart_obj.save()
        return redirect(request.META['HTTP_REFERER'])
