from django.contrib import messages
from django.shortcuts import redirect


from apps.coupons.models import Coupon, UsedCoupon


def check_coupon(request):

    code = request.POST.get('coupon_code')

    try:
        coupon = Coupon.objects.get(code=code)

    except Coupon.DoesNotExist:
        if request.session.get('coupon_code'):
            del request.session['coupon_code']

        messages.error(request, 'not valid coupon')
    else:

        if UsedCoupon.objects.filter(coupon_id=coupon.pk, user_id=request.user.pk).exists():
            if request.session.get('coupon_code'):
                del request.session['coupon_code']

            messages.warning(request, 'this coupon has alredy')
        else:
            request.session['coupon_data'] = {
                'code': code,
                'discount_percent': coupon.discount_percent
            }
            messages.success(request, 'is valid coupon')

    return redirect(request.META['HTTP_REFERER'])
