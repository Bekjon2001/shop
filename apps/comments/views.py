from django.shortcuts import render, redirect
from django.contrib import messages

from apps.comments.forms import CommentCreateForm


def create_comment(request):
    if request.method == 'GET':
        return redirect('home_pege')
    form = CommentCreateForm(data=request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your comment has been create')
    else:
        messages.error(request, form.errors)
    return redirect(request.META['HTTP_REFERER'])
