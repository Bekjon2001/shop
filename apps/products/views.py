from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from apps.comments.models import ProductComment
from apps.products.models import Product,ProductFeatures
from apps.wishlist.models import Wishlist

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = ProductComment.objects.filter(product_id=product.pk).order_by('-created_at')

    paginator = Paginator(comments, 3)
    comment_page = request.GET.get('comment_page', 1)
    comment_page_obj = paginator.get_page(comment_page)
    product_features = ProductFeatures.objects.filter(product_id=pk)

    context = {
        'product': product,
        'comments': comments,
        'comment_page_obj': comment_page_obj,
        'product_features': product_features,
        'page': 'detail'
    }
    return render(request=request, template_name='detail.html', context=context)


def product_by_feature(request, pk):
    print(request.POST)
    return redirect('products:detail-page', pk=pk)


def product_list(request: WSGIRequest) -> HttpResponse:

    user = request.user
    if user.is_authenticated:
        user_wishlist = Wishlist.objects.filter(user_id=user.pk).values_list('product_id', flat=True)
    else:
        user_wishlist = []

    search_text = request.session.get('search_text', None)
    queryset = Product.objects.order_by('-pk')
    sort_by = request.GET.get('latest')

    if search_text:
        queryset = queryset.filter(title__icontains=search_text)
    if sort_by == 'latest':
        queryset = queryset.order_by('-created_at')  # So'nggi qo'shilgan mahsulotlar
    elif sort_by == 'popularity':
        if hasattr(Product, 'sales_count'):  # Agar `sales_count` maydoni mavjud bo'lsa
            queryset = queryset.order_by('-sales_count')  # Eng ko'p sotilgan mahsulotlar
        else:
            queryset = queryset.none()  # Agar `sales_count` bo'lmasa, bo'sh queryset qaytarish
    elif sort_by == 'best_rating':
        if hasattr(Product, 'avg_rating'):  # Agar `avg_rating` maydoni mavjud bo'lsa
            queryset = queryset.order_by('-avg_rating')  # Eng yaxshi reytingga ega mahsulotlar
        else:
            queryset = queryset.none()  # Agar `avg_rating` bo'lmasa, bo'sh queryset qaytarish
    else:
        queryset = queryset.order_by('-created_at')  # Standart tartib, 'latest'

    # Agar hech qanday mahsulot topilmasa, foydalanuvchiga xabar berish
    if not queryset.exists():
        context = {
            'message': 'No products found matching your criteria.'
        }
        return render(request, 'shop.html', context)

    page_number = request.GET.get('page', 1)
    paginate_obj = Paginator(queryset, 9)
    page_obj = paginate_obj.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'page': 'shop',
        'user_wishlist': user_wishlist,
        'sort_by':sort_by

    }
    return render(request=request, template_name='shop.html', context=context)
