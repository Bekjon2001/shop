from apps.categories.models import Category
from apps.general.models import General, GeneralSocialMedia
from apps.wishlist.models import Wishlist


def general_context(request):
    context = {
        'general': General.objects.all(),
        'categories': Category.objects.select_related('parent').filter(parent__isnull=False),
        'general_social_media': GeneralSocialMedia.objects.all(),
        'wishlist': Wishlist.objects.all(),
        'currency': request.session.get('currency', General.DEFAULT_CURRENCY),
        'currency_list': General.Currency.labels
    }
    return context