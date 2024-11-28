from django.shortcuts import redirect, render
from django.utils.translation import activate, get_language
from django.views import View

from config import settings
from django.core.paginator import Paginator

from apps.general.models import General
from apps.wishlist.models import Wishlist
from apps.products.models import Product


class HomeView(View):
    def get(self,request):
        queryset = Product.objects.order_by('-avg_rating')
        page_number = request.GET.get('page', 1)
        paginator = Paginator(queryset, 8)
        page_obj = paginator.get_page(page_number)
        context = {
            'wishlist': Wishlist.objects.all(),
            'page_obj': page_obj,
            'page': 'home',
        }
        return render(request, template_name='index.html', context=context)


class SetLanguageView(View):
    def get(self,request, lang):
        if not lang in settings.MODELTRANSLATION_LANGUAGES:
            lang = settings.LANGUAGE_CODE
        activate(lang)
        host = request.build_absolute_uri('/')
        redirect_to = host + lang + request.META['HTTP_REFERER'].replace(host, '')[2:]
        return redirect(redirect_to)

class SetCurrencyView(View):
    def get(self,request, currency: str):
        currencies = General.Currency.values
        print(currency)
        if currency in currencies:
            request.session['currency'] = currency
        return redirect(request.META['HTTP_REFERER'])

class SearchView(View):
    def get(self,request):
        search_text = request.GET.get('search', '')
        request.session['search_text'] = search_text
        return redirect('products:product_list')

class FlushSessionView(View):
    def get(self,request):
        request.session.flush()
        return redirect(request.META['HTTP_REFERER'])
