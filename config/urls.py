from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from apps.contact.views import ContactView
from apps.general.views import (
    SetLanguageView,
    HomeView,
    SearchView,
    SetCurrencyView,
    FlushSessionView
)

urlpatterns = [
    # CKEditor URLs
    path("__ckeditor5/", include('django_ckeditor_5.urls')),

    # Media URLs
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),

    # Set Language and Currency URLs
    path('set-language/<str:lang>/', SetLanguageView.as_view(), name='set-lang'),
    path('set-currency/<str:currency>/', SetCurrencyView.as_view(), name='set-curr'),

    # Other static or dynamic URLs can go here
]

# Add internationalization patterns
urlpatterns += i18n_patterns(
    path('', HomeView.as_view(), name='home-page'),
    path('admin/', admin.site.urls),

    # General URLs
    path('checkout/', include('apps.orders.urls')),
    path('search/', SearchView.as_view(), name='search'),
    path('flush/', FlushSessionView.as_view(), name='flush'),

    # Other app URL patterns
    path('cart/', include('apps.carts.urls', namespace='carts')),
    path('coupons/', include('apps.coupons.urls', namespace='coupons')),
    path('contact/', ContactView.as_view(), name='contact-page'),
    path('comments/', include('apps.comments.urls', namespace='comments')),
    path('category/', include('apps.categories.urls')),
    path('about/', include('apps.abouts.urls', namespace='about')),
    path('wishlist/', include('apps.wishlist.urls', namespace='wishlists')),
    path('products/', include('apps.products.urls', namespace='products')),
    path('auth/', include('apps.authentication.urls')),

    # Debug toolbar
    path('__debug__/', include('debug_toolbar.urls')),
)

