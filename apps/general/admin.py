from django.contrib import admin
from apps.general.models import General,PaymentMethod

@admin.register(General)
class AdminGeneral(admin.ModelAdmin):

    def has_add_permission(self, request):
        return not General.objects.exists()

@admin.register(PaymentMethod)
class AdminPaymentMethod(admin.ModelAdmin):
    pass

