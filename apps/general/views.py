from django.shortcuts import redirect, render
from django.utils.translation import activate, get_language

from config import settings
from django.core.paginator import Paginator

from apps.general.models import General
from apps.wishlist.models import Wishlist
from apps.products.models import Product



def home(request):
    queryset = Product.objects.all().order_by('-pk')  # Mahsulotlarni so'nggi qo'shilgan tartibda olish

    # Sahifalash
    page_number = request.GET.get('page', 1)  # URL parametridan sahifa raqamini olish
    paginator = Paginator(queryset, 8)  # 8 ta mahsulotni har sahifada ko'rsatish
    page_obj = paginator.get_page(page_number)
    context = {
        'wishlist': Wishlist.objects.all(),
        'page_obj': page_obj,
        'page': 'home',
    }
    return render(request, template_name='index.html', context=context)


def checkout(request):
    return render(request=request, template_name='checkout.html', context={'page': 'pages'})


def cart(request):
    return render(request=request, template_name='cart.html', context={'page': 'pages'})


def set_language(request, lang):
    if not lang in settings.MODELTRANSLATION_LANGUAGES:
        lang = settings.LANGUAGE_CODE
    activate(lang)
    host = request.build_absolute_uri('/')
    redirect_to = host + lang + request.META['HTTP_REFERER'].replace(host, '')[2:]
    return redirect(redirect_to)


def set_currency(request, currency: str):
    currencies = General.Currency.values
    print(currency)
    if currency in currencies:
        request.session['currency'] = currency
    return redirect(request.META['HTTP_REFERER'])


def search(request):
    search_text = request.GET.get('search', '')
    request.session['search_text'] = search_text
    return redirect('products:product_list')


def flush_session(request):
    request.session.flush()
    return redirect(request.META['HTTP_REFERER'])
