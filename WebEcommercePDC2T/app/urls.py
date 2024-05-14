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

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset_form.html'), name= 'password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name= 'password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html'), name= 'password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name= 'password_reset_complete'),

    path('search/', views.search, name= 'search'),
    path('<str:cateName>/price/<str:price_range>/', views.product, name="product_price_filter"),

    path('blog/', views.blog, name="blog"),
    path('blogDetail/', views.blogDetail, name="blogDetail"),
    path('checkout/', views.checkout, name="checkout"),
    path('cart/', views.cart, name="cart"),
    path('product/', views.product, name="product"),
    path('productDetail/', views.productDetail, name="productDetail"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('profile/', views.profile, name="profile"),
]