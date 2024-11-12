from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.abouts.models import About


@login_required
def about(request):
    context = {
        'about': About.objects.first(),
        'page': 'about'
    }

    return render(request, 'about.html', context)



