from django.contrib import admin
from apps.coupons.models import Coupon

@admin.register(Coupon)
class AdminCoupon(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False
