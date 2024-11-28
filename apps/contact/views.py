from django.contrib import messages
from django.views import View

from apps.contact.forms import ContactForm
from django.shortcuts import render

class ContactView(View):
    def post(self,request):
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Malumot jo'natildi")
        else:
            messages.error(request,form.errors)
        return render(request,'contact.html')
    def get(self, request):
        return render(request, "contact.html")