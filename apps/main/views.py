from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, get_user_model, logout
from apps.main.forms import UserRegistrationForm


@login_required(login_url='login-page')
def home(request):
    return render(request, template_name='index.html')


def shop(request):
    return render(request=request, template_name='shop.html',context={'page':'shop'})


def detail(request):
    return render(request=request, template_name='detail.html',context={'page':'detail'})


def contact(request):
    return render(request=request, template_name='contact.html',context={'page':'contact'})


def checkout(request):
    return render(request=request, template_name='checkout.html',context={'page':'pages'})


def cart(request):
    return render(request=request, template_name='cart.html',context={'page':'pages'})


def about(request):
    return render(request=request, template_name='about.html',context={'page':'about'})


def login_page(request):
    return render(request=request,template_name= 'auth-login-basic.html')


def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if not user:
        messages.error(request, 'Invalid username or password.')
        return redirect('login-page')
    login(request, user)
    return redirect('home-page')

def logout_page(request):
    logout(request)
    return redirect('login-page')

def register_page(request):
    form = UserRegistrationForm()
    return render(request, 'auth-register-basic.html', {'form': form})


def user_register(request):
    obj_register = UserRegistrationForm(request.POST)
    if obj_register.is_valid():
        messages.success(request, 'Account was created successfully.')
        get_user_model().objects.create_user(**obj_register.cleaned_data)
    else:
        messages.error(request, obj_register.errors)
        return redirect('register-page')
    return redirect('login-page')
