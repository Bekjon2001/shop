from django.shortcuts import  redirect
from django.contrib import messages
from django.views import View
from django.views.generic import CreateView

from apps.comments.forms import CommentCreateForm

class CommentCreateView(View):
    def post(self,request):
        form = CommentCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment has been create')
        else:
            messages.error(request, form.errors)
        return redirect(request.META['HTTP_REFERER'])
