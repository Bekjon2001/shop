from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from apps.abouts.models import About


# @login_required
# def about(request):
#     context = {
#         'about': About.objects.first(),
#         'page': 'about'
#     }
#
#     return render(request, 'about.html', context)
class AboutView(View,LoginRequiredMixin):
    def get(self, request):
        context = {
            'about': About.objects.first(),
            'page': 'about'
        }

        return render(request, 'about.html', context)


