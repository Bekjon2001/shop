
from django.urls import path

from apps.abouts.views import AboutView

app_name='about'

urlpatterns = [
    path('', AboutView.as_view() , name='about-page'),
]