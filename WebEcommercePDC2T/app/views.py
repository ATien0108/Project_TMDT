from django.db import connection
from django.http import JsonResponse
import matplotlib.pyplot as plt
from httpx import Auth
from django.conf import settings
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, authenticate, login as auth_login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime, date
from .forms import *
from django.contrib.auth.models import User
from django.urls import reverse
from django.urls import reverse_lazy
from .models import Product, Category, Brand, CartItem, PaymentMethod, Order, OrderItem, InforDelivery, Payment
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import QueryDict   

# Create your views here.
def home(request):
    # Lấy tất cả các danh mục
    categories = Category.objects.all()
    brands = Brand.objects.all()
    context = {
        'categories': categories,
        'brands': brands
    }
    return render(request, 'app/home.html', context)


def blog(request):
    all_blogs = Blog.objects.all() 
    paginator = Paginator(all_blogs, 8)  # Số lượng bài blog trên mỗi trang
    page_number = request.GET.get('page')  # Lấy số trang hiện tại từ query parameter 'page'
    page_obj = paginator.get_page(page_number)  # Lấy object paginator cho trang hiện tại
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'app/blog.html', context)

def blogDetail(request, blogTitle):
    blog = get_object_or_404(Blog, blogTitle=blogTitle)
    blog_details = BlogDetails.objects.filter(blog=blog)
    context = {
        'blog': blog,
        'blog_details': blog_details,
    }
    return render(request, 'app/blogDetail.html', context)

def search(request):
    searched = ''
    keys = None
    if request.method == "POST":
        searched = request.POST["searched"]
        # Thực hiện truy vấn không phân biệt chữ hoa chữ thường
        keys = Product.objects.filter(Q(proName__icontains=searched))
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

@login_required
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    payment_methods = PaymentMethod.objects.all()

    # Calculate order summary
    subtotal = sum(item.pro.proPrice * item.quantity for item in cart_items)
    shipping = 2.0  # example shipping cost
    tax = 1.0  # example tax cost
    total = subtotal + shipping + tax

    cart_items_with_images = []
    for item in cart_items:
        images = item.pro.image_set.all()
        if images.exists():
            image_url = images[0].image_file.url if images[0].image_file else images[0].image_url
        else:
            image_url = None  # or set a default image URL
        cart_items_with_images.append((item, image_url))

    if request.method == "POST":
        # Get user input data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        phone_number = request.POST.get('phone_number')
        district = request.POST.get('district')
        province = request.POST.get('province')
        payment_method_id = request.POST.get('payment_method')

        # Check for missing fields
        required_fields = ['first_name', 'last_name', 'email', 'street', 'phone_number', 'district', 'province', 'payment_method_id']
        if not all(request.POST.get(field) for field in required_fields):
            return render(request, 'app/checkout.html', {
                'cart_items_with_images': cart_items_with_images,
                'payment_methods': payment_methods,
                'subtotal': subtotal,
                'shipping': shipping,
                'tax': tax,
                'total': total,
                'error': 'All fields are required.'
            })

        try:
            # Create Order
            order = Order.objects.create(
                user=user,
                orderDate=date.today(),
                orderStatus='pending'
            )

            # Create OrderItems
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    pro=cart_item.pro,
                    proPrice=cart_item.pro.proPrice,
                    proQuantity=cart_item.quantity
                )

            # Create Payment
            payment_method = PaymentMethod.objects.get(id=payment_method_id)
            payment = Payment.objects.create(
                order=order,
                paymentDate=date.today(),
                paymentStatus='unpaid',
                payMethod=payment_method
            )

            # Create InforDelivery
            infor_delivery = InforDelivery.objects.create(
                order=order,
                receiverName=f"{first_name} {last_name}",
                province=province,
                district=district,
                street=street,
                phoneNumber=phone_number
            )

            # Clear cart items
            cart_items.delete()

            messages.success(request, 'Your order has been placed successfully!')
            return redirect('home')  # Redirect to a success page or home

        except Exception as e:
            # Rollback: Delete the order, payment, and delivery information if an error occurs
            order.delete() if order else None
            payment.delete() if payment else None
            infor_delivery.delete() if infor_delivery else None

            error_message = f'Error processing order: {str(e)}'
            messages.error(request, error_message)

    context = {
        'cart_items_with_images': cart_items_with_images,
        'payment_methods': payment_methods,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total
    }
    return render(request, 'app/checkout.html', context)

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')

def cart(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_cart_items = CartItem.objects.filter(user=request.user)
        
            cart_items = []
            for cart_item in user_cart_items:
                product = Product.objects.get(pk=cart_item.pro_id)
                cart_items.append((cart_item, product))
            
            context = {
                'cart_items': cart_items
            }
            return render(request, 'app/cart.html', context)
        else:
            return redirect('login')

    elif request.method == 'POST':
        if request.user.is_authenticated:
            product_id = request.POST.get('product_id') 
            quantity = int(request.POST.get('quantity', 1))
            product = get_object_or_404(Product, pk=product_id)
            
            user = request.user
            cart_item = CartItem.objects.filter(user_id=user.id, pro_id=product.pro_id).first()
            
            if cart_item is not None:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(user_id=user.id, pro_id=product.pro_id, quantity=quantity)
            
            unique_item_count = CartItem.objects.filter(user=user).count()
            return JsonResponse({'message': 'Product added to cart successfully.', 'unique_item_count': unique_item_count})
        else:
            return JsonResponse({'redirect': '/login/'})

    elif request.method == 'PUT':
        put_data = QueryDict(request.body)

        cart_item_id = put_data.get('cart_item_id')
        new_quantity = int(put_data.get('new_quantity', 1))

        cart_item = get_object_or_404(CartItem, cartItem_id=cart_item_id)
        cart_item.quantity = new_quantity
        cart_item.save()
        
        unique_item_count = CartItem.objects.filter(user=request.user).count()
        return JsonResponse({'success': True, 'unique_item_count': unique_item_count})

    elif request.method == 'DELETE':
        put_data = QueryDict(request.body)

        if 'clear_cart' in put_data:
            user = request.user
            CartItem.objects.filter(user=user).delete()
            return JsonResponse({'success': True, 'unique_item_count': 0})
        else:
            cart_item_id = put_data.get('cart_item_id')
            cart_item = get_object_or_404(CartItem, cartItem_id=cart_item_id)
            cart_item.delete()
            
            unique_item_count = CartItem.objects.filter(user=request.user).count()
            return JsonResponse({'success': True, 'unique_item_count': unique_item_count})

    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE'])

def get_cart_quantity(request):
    cart_quantity = CartItem.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    return JsonResponse({'cart_quantity': cart_quantity})

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

def brand_product(request, braName, price_range=None):
    brand = get_object_or_404(Brand, braName=braName)
    products = Product.objects.filter(brand=brand)

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
            
    context = {'products': products, 'brand': brand}
    return render(request, 'app/brand_product.html', context)

def productDetail(request, proName):
    
    product = get_object_or_404(Product, proName = proName)
    product_specs = ProductSpecification.objects.filter(product=product)

    context = {
        'product': product,
        'product_specs': product_specs,
    }
    
    return render(request, 'app/productDetail.html', context)

def profile(request):
    return render(request, 'app/profile.html')