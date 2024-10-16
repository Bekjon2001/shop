from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404

from apps.comments.models import ProductComment
from apps.products.models import Product
from apps.wishlist.models import Wishlist


from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = ProductComment.objects.filter(product_id=product.pk).order_by('-created_at')

    paginator = Paginator(comments, 3)
    comment_page = request.GET.get('comment_page', 1)
    comment_page_obj = paginator.get_page(comment_page)

    context = {
        'product': product,
        'comments': comments,
        'comment_page_obj': comment_page_obj,
        'page': 'detail'
    }
    return render(request=request, template_name='detail.html', context=context)

def product_list(request: WSGIRequest) -> HttpResponse:
    user = request.user
    if user.is_authenticated:
        user_wishlist = Wishlist.objects.filter(user_id=user.pk).values_list('product_id', flat=True)
    else:
        user_wishlist = []

    search_text = request.session.get('search_text', None)
    queryset = Product.objects.order_by('-pk')

    if search_text:
        queryset = queryset.filter(title__icontains=search_text)

    page_number = request.GET.get('page', 1)
    paginate_obj = Paginator(queryset, 9)
    page_obj = paginate_obj.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'page': 'shop',
        'user_wishlist': user_wishlist
    }
    return render(request=request, template_name='shop.html', context=context)
