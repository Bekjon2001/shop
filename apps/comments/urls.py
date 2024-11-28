from django.urls import path

from apps.comments.views import CommentCreateView

app_name = 'comments'

urlpatterns = [
    path('create/',CommentCreateView.as_view(), name='create_comment'),
    ]