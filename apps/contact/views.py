from django.contrib import messages
from django.shortcuts import render, redirect

from apps.contact.forms import ContactForm

#
# def contact(request):
#         obj_register = ContactForm(request.POST)
#         if obj_register.is_valid():
#             messages.success(request, 'Account was created successfully.')
#             get_user_model().objects.create_user(**obj_register.cleaned_data)
#         else:
#             messages.error(request=request, message=obj_register.errors)
#             return redirect('register-page')
#         return redirect('login-page')
#
#     return render(request=request, template_name='contact.html', context={'page': 'contact'})
from django.http import HttpResponseRedirect
from django.shortcuts import render


def contact(request):
    if request.method == "POST":
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Malumot jo'natildi")
        else:
            messages.error(request,form.errors)


    return render(request, "contact.html")