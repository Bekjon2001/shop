from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


from apps.contact.views import contact
from apps.categories.views import category
from apps.general.views import (
    set_language,
    home,
    search,
    set_currency,
    flush_session
)

urlpatterns = [
    # =========== CKEDITOR URLS  ============
    path("__ckeditor5/", include('django_ckeditor_5.urls')),

    # =============MEDIA URLS===========
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),

    # =======SET LANGUAGE URLS =======
    path('set-language/<str:lang>/', set_language, name='set-lang'),

    # =======SET CURRENCY URLS =======
    path('set-currency/<str:currency>/', set_currency, name='set-curr'),

]
urlpatterns += i18n_patterns(
    path('', home, name='home-page'),
    path('admin/', admin.site.urls),

    # ======= General URLS =======

    path('checkout/',include('apps.orders.urls')),
    path('search/', search, name='search'),
    path('flush/', flush_session,name='flush'),

    #========== CART URLS ==============
    path('cart/', include('apps.carts.urls',namespace='carts')),

    #============ COUPON URLS ==========
    path('coupons/', include('apps.coupons.urls',namespace='coupons')),


    # ============= CONTACT URLS =============
    path('contact/', contact, name='contact-page'),

    # ============= COMMENTS URLS =============
    path('comments/', include('apps.comments.urls', namespace='comments' )),

    # ============= CATEGORIES URLS =============
    path('category/', category, name='category'),

    # ============= ABOUT URLS =============
    path('about/', include('apps.abouts.urls', namespace='about')),

    # ============= WISHLIST URLS =============
    path('wishlist/', include('apps.wishlist.urls', namespace='wishlists')),

    # =============  PRODUCTS URLS =============
    path('products/', include('apps.products.urls', namespace='products')),

    # ============= AUTH URLS  =============
    path('auth/', include('apps.authentication.urls')),

    # ============= DEBUG_TOOLBAR URLs =============
    path('__debug__/', include('debug_toolbar.urls')),

)
