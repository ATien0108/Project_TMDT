from django.db import connection
from django.http import JsonResponse
import numpy as np
import matplotlib.pyplot as plt
from httpx import Auth
import os
from django.conf import settings
from .models import *
import mpld3
from django.contrib.auth import update_session_auth_hash, authenticate, login as auth_login, logout
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import Group
from datetime import datetime
from .forms import *
from django.contrib.auth.models import User
from django.urls import reverse
from django.urls import reverse_lazy
from .models import Product, Category, Brand
from django.contrib.auth.hashers import check_password

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def blog(request):
    return render(request, 'app/blog.html')

def blogDetail(request):
    return render(request, 'app/blogDetail.html')

def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(proName__contains = searched)
    return render(request, 'app/search.html', {"searched":searched, "keys":keys})

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)
            request.session['logged_in_user'] = user.username
            # Tiếp tục kiểm tra group và chuyển hướng
            if user.groups.filter(name='admin').exists():
                return redirect('/admin')
            else:
                return redirect('home')
        else:
            messages.info(request, 'Username or password not correct!')

    context = {}
    return render(request, 'app/login.html', context)

def signup(request):
    form = RegisterForm()
    success_message = None

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.source = 'Register'
            user.save()
            success_message = "Đăng ký tài khoản thành công"
            return redirect(reverse('login'))  # Chuyển hướng đến trang chính của ứng dụng, thay 'home' bằng tên đường dẫn của trang bạn muốn chuyển hướng đến.

    context = {'form': form, 'success_message': success_message}
    return render(request, 'app/signup.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def checkout(request):
    return render(request, 'app/checkout.html')

def cart(request):
    return render(request, 'app/cart.html')

def product(request, cateName, price_range=None):
    category = get_object_or_404(Category, cateName=cateName)
    products = Product.objects.filter(cate=category)

    if price_range:
        if price_range == 'under_1tr':
            products = products.filter(proPrice__lt=1000000)
        elif price_range == '1tr_3tr':
            products = products.filter(proPrice__gte=1000000, proPrice__lt=3000000)
        elif price_range == '3tr_5tr':
            products = products.filter(proPrice__gte=3000000, proPrice__lt=5000000)
        elif price_range == '5tr_7tr':
            products = products.filter(proPrice__gte=5000000, proPrice__lt=7000000)
        elif price_range == 'above_7tr':
            products = products.filter(proPrice__gte=7000000)

    context = {'products': products, 'category': category}

    return render(request, 'app/product.html', context)

def productDetail(request):
    return render(request, 'app/productDetail.html')

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')

def profile(request):
    return render(request, 'app/profile.html')