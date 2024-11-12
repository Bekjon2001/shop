from django.shortcuts import render

def checkout(request):
    return render(request=request, template_name='checkout.html', context={'page': 'pages'})
