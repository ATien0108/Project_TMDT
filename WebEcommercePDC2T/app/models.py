from django import forms
from django.db import models
import random
from django.contrib.auth.forms import UserCreationForm
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.db import connection
from django.dispatch import receiver
from django.contrib.auth.models import User

class Brand(models.Model):
    bra_id = models.BigAutoField(primary_key=True)
    braName = models.CharField(max_length=100)
    braImage = models.ImageField(upload_to="brand_images/", blank=True, null=True)

    def __str__(self):
        return self.braName

class Category(models.Model):
    cate_id = models.BigAutoField(primary_key=True)
    cateName = models.CharField(max_length=255)
    cateWarranty = models.IntegerField()

    def __str__(self):
        return self.cateName

class Product(models.Model):
    pro_id = models.BigAutoField(primary_key=True)
    proName = models.CharField(max_length=255)
    proDescription = models.TextField()
    proPrice = models.FloatField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    cate = models.ForeignKey(Category, on_delete=models.CASCADE)
    proManufature = models.IntegerField()

    def __str__(self):
        return self.proName

class ProductSpecification(models.Model):
    prod_spec_id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    spec1 = models.CharField(max_length=255, blank=True, null=True)
    spec2 = models.CharField(max_length=255, blank=True, null=True)
    spec3 = models.CharField(max_length=255, blank=True, null=True)
    spec4 = models.CharField(max_length=255, blank=True, null=True)
    spec5 = models.CharField(max_length=255, blank=True, null=True)
    spec6 = models.CharField(max_length=255, blank=True, null=True)
    spec7 = models.CharField(max_length=255, blank=True, null=True)
    spec8 = models.CharField(max_length=255, blank=True, null=True)
    spec9 = models.CharField(max_length=255, blank=True, null=True)
    spec10 = models.CharField(max_length=255, blank=True, null=True)
    spec11 = models.CharField(max_length=255, blank=True, null=True)
    spec12 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.product.proName} Specifications"


class Image(models.Model):
    pro = models.ForeignKey(Product, on_delete=models.CASCADE)
    img_id = models.BigAutoField(primary_key=True)
    image_file = models.ImageField(upload_to="product_images/", blank=True, null=True)  # Trường để lưu trữ hình ảnh tải lên
    image_url = models.URLField(blank=True, null=True)  # Trường để lưu trữ URL của hình ảnh

    def __str__(self):
        return self.image_file.url if self.image_file else self.image_url
    
class CartItem(models.Model):
    cartItem_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pro = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inforDeli = models.ForeignKey('InforDelivery', on_delete=models.CASCADE)
    orderDate = models.DateField()
    orderStatus = models.CharField(max_length=255)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE)

class OrderItem(models.Model):
    orderItem_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pro = models.ForeignKey(Product, on_delete=models.CASCADE)
    proPrice = models.FloatField()
    proQuantity = models.IntegerField()

class InforDelivery(models.Model):
    inforDeli_id = models.BigAutoField(primary_key=True)
    receiverName = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=20)

class Payment(models.Model):
    payment_id = models.BigAutoField(primary_key=True)
    paymentDate = models.DateField()
    paymentStatus = models.CharField(max_length=255)
    payMethod = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE)

class PaymentMethod(models.Model):
    payMethod_id = models.BigAutoField(primary_key=True)
    payName = models.CharField(max_length=255)

class Rating(models.Model):
    rate_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pro = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField()

class Blog(models.Model):
    blog_id = models.BigAutoField(primary_key=True)
    blogTitle = models.CharField(max_length=255)
    blogContent = models.TextField()
    blogDate = models.DateField()
    image_file = models.ImageField(upload_to="blog_images/", blank=True, null=True)  # Trường để lưu trữ hình ảnh tải lên
    image_url = models.URLField(blank=True, null=True)  # Trường để lưu trữ URL của hình ảnh

    def __str__(self):
        return self.blogTitle

class BlogDetails(models.Model):
    blogDel_id = models.BigAutoField(primary_key=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='details')
    blogDelTitle = models.CharField(max_length=255)
    image_file = models.ImageField(upload_to="blog_details_images/", blank=True, null=True)  # Trường để lưu trữ hình ảnh tải lên
    image_url = models.URLField(blank=True, null=True)  # Trường để lưu trữ URL của hình ảnh
    description = models.TextField()

    def __str__(self):
        return self.blogDelTitle