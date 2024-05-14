from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logoutPage, name= 'logout'),
    path('forgotpass/', views.forgotpass, name="forgotpass"),
    path('reset_password/', views.reset_password, name="reset_password"),
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