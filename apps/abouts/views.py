from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.abouts.models import About


@login_required
def about(request):
    perm = 'Abouts pachni kurish'
    user_permissions = request.user.user_permissions.values_list('title', flat=True)

    if not request.user.is_superuser and perm not in user_permissions:
        return render(request, '403.html', {'message': 'Sizning ushbu sahifaga kirish huquqingiz yo\'q.'})
 
    context = {
        'about': About.objects.first(),
        'page': 'about'
    }

    return render(request, 'about.html', context)



