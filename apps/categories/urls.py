from django.urls import path
from apps.categories.views import CategoryView,SetCategoryView

urlpatterns = [
    path('', CategoryView.as_view(), name='category'),
    path('set-category/<int:cat_id>/', SetCategoryView.as_view(), name='set-category')
]