from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logoutPage, name= 'logout'),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('profile/', views.profile, name="profile"),
    path('update_file/', views.update_profile, name="update_profile"),

    path('cs-bao-mat/', views.csBaoMat, name='cs-bao-mat'),
    path('cs-bao-hanh/', views.csBaoHanh, name='cs-bao-hanh'),
    path('cs-van-chuyen/', views.csVanChuyen, name='cs-van-chuyen'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset_form.html'), name= 'password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name= 'password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html'), name= 'password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name= 'password_reset_complete'),

    path('search/', views.search, name= 'search'),
    path('<str:cateName>/price/<str:price_range>/', views.product, name="product_category_price_filter"),

    path('blog/', views.blog, name="blog"),
    path('blogDetail/<str:blogTitle>/', views.blogDetail, name='blogDetail'),
    path('brand/<str:braName>/price/<str:price_range>/', views.brand_product, name="product_brand_price_filter"),

    path('checkout/', views.checkout, name="checkout"),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    
    path('cart/', views.cart, name="cart"),
    path('cart-quantity/', views.get_cart_quantity, name='get_cart_quantity'),
    
    path('<str:cateName>/', views.product, name="product"),
    path('brand/<str:braName>/', views.brand_product, name="brand_product"),
    path('productDetail/<str:proName>/', views.productDetail, name='productDetail'),
    path('reviewPage/<int:product_id>/', views.review_Page, name='review_Page'),
    path('reviewPage/review/<int:product_id>/', views.add_review, name='add_review'),

]