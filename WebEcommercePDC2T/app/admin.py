from django.contrib import admin
from django.utils.html import format_html
from .models import Brand, Category, Product, Image, Blog, BlogDetails, CartItem, Order, OrderItem, InforDelivery, Payment, PaymentMethod, Rating, ProductSpecification
import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import DateFieldListFilter

class BrandAdmin(admin.ModelAdmin):
    list_display = ('bra_id', 'braName', 'display_image')
    search_fields = ('braName',)  # Add search functionality for brand name

    def display_image(self, obj):
        if obj.braImage:
            return format_html('<img src="{}" width="60" height="60" />', obj.braImage.url)
        return 'No Image'
    display_image.short_description = 'Image'

admin.site.register(Brand, BrandAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cate_id', 'cateName', 'cateWarranty')
    search_fields = ('cateName',)  # Add search functionality for category name

admin.site.register(Category, CategoryAdmin)

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class ProductSpecificationInline(admin.StackedInline):
    model = ProductSpecification
    extra = 0

class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('prod_spec_id', 'product', 'title', 'spec')
    search_fields = ('product__proName', 'title', 'spec')
    list_filter = ('product__proName',)

admin.site.register(ProductSpecification, ProductSpecificationAdmin)

class PriceRangeFilter(admin.SimpleListFilter):
    title = 'price range'
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return [
            ('0-500000', '$0 - $500.000'),
            ('500000-1000000', '$500.000 - $1.000.000'),
            ('1000000-5000000', '$1.000.000 - $5.000.000'),
            ('5000000-10000000', '$5.000.000 - $10.000.000'),
            ('10000000+', '$10.000.000+'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '0-500000':
            return queryset.filter(proPrice__gte=0, proPrice__lt=500000)
        elif self.value() == '500000-1000000':
            return queryset.filter(proPrice__gte=500000, proPrice__lt=1000000)
        elif self.value() == '1000000-5000000':
            return queryset.filter(proPrice__gte=1000000, proPrice__lt=5000000)
        elif self.value() == '5000000-10000000':
            return queryset.filter(proPrice__gte=5000000, proPrice__lt=10000000)
        elif self.value() == '10000000+':
            return queryset.filter(proPrice__gte=10000000)
        return queryset

class ProductAdmin(admin.ModelAdmin):
    list_display = ('pro_id', 'proName', 'proDescription', 'proPrice', 'get_brand_name', 'get_category_name', 'proManufature', 'display_image')
    inlines = [ImageInline, ProductSpecificationInline]
    search_fields = ('proName', 'proDescription', 'brand__braName', 'cate__cateName')  # Add search functionality for product name, description, brand name, and category name
    list_filter = ('brand__braName', 'cate__cateName', 'proManufature', PriceRangeFilter)  # Add filtering functionality

    def get_brand_name(self, obj):
        return obj.brand.braName
    get_brand_name.short_description = 'Brand'

    def get_category_name(self, obj):
        return obj.cate.cateName
    get_category_name.short_description = 'Category'

    def display_image(self, obj):
        image = obj.image_set.first()
        if image:
            if image.image_file:
                return format_html('<img src="{}" width="60" height="60" />', image.image_file.url)
            elif image.image_url:
                return format_html('<img src="{}" width="60" height="60" />', image.image_url)
        return 'No Image'
    display_image.short_description = 'Image'

admin.site.register(Product, ProductAdmin)

class BlogDetailsInline(admin.TabularInline):
    model = BlogDetails
    extra = 1
    fields = ('blogDelTitle', 'description', 'image_file', 'image_url')

class WeekFilter(admin.SimpleListFilter):
    title = 'week'
    parameter_name = 'week'

    def lookups(self, request, model_admin):
        weeks = []
        current_year = datetime.date.today().year
        for week in range(1, 53):
            start_date = datetime.date.fromisocalendar(current_year, week, 1)
            end_date = start_date + datetime.timedelta(days=6)
            weeks.append((week, '{} ({} to {})'.format(week, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))))
        return weeks

    def queryset(self, request, queryset):
        if self.value():
            week_number = int(self.value())
            current_year = datetime.date.today().year
            start_date = datetime.date.fromisocalendar(current_year, week_number, 1)
            end_date = start_date + datetime.timedelta(days=6)
            return queryset.filter(blogDate__range=[start_date, end_date])
        return queryset

class BlogAdmin(admin.ModelAdmin):
    list_display = ('blog_id', 'blogTitle', 'blogDate', 'display_image')
    search_fields = ('blogTitle', 'blogContent', 'blogDate')
    list_filter = (WeekFilter,)  # Add the custom filter here
    fields = ('blogTitle', 'blogContent', 'blogDate', ('image_file', 'image_url'))
    inlines = [BlogDetailsInline]

    def display_image(self, obj):
        if obj.image_file:
            return format_html('<img src="{}" width="60" height="60" />', obj.image_file.url)
        elif obj.image_url:
            return format_html('<img src="{}" width="60" height="60" />', obj.image_url)
        return 'No Image'
    display_image.short_description = 'Image'

admin.site.register(Blog, BlogAdmin)

class BlogDetailsAdmin(admin.ModelAdmin):
    list_display = ('blogDel_id', 'get_blog_title', 'blogDelTitle', 'display_image', 'description')
    search_fields = ('blogDelTitle', 'description', 'blog__blogTitle')
    list_filter = ('blog__blogTitle',)  # Add filter for Blog title
    fields = ('blogDelTitle', ('image_file', 'image_url'), 'description')

    def get_blog_title(self, obj):
        return obj.blog.blogTitle
    get_blog_title.short_description = 'Blog Title'

    def display_image(self, obj):
        if obj.image_file:
            return format_html('<img src="{}" width="60" height="60" />', obj.image_file.url)
        elif obj.image_url:
            return format_html('<img src="{}" width="60" height="60" />', obj.image_url)
        return 'No Image'
    display_image.short_description = 'Image'

admin.site.register(BlogDetails, BlogDetailsAdmin)

class QuantityRangeFilter(admin.SimpleListFilter):
    title = 'quantity range'
    parameter_name = 'quantity_range'

    def lookups(self, request, model_admin):
        return [
            ('0-1', '0 to 1'),
            ('1-3', '1 to 3'),
            ('3-5', '3 to 5'),
            ('5-10', '5 to 10'),
            ('10+', '10+'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '0-1':
            return queryset.filter(quantity__gte=0, quantity__lt=1)
        elif self.value() == '1-3':
            return queryset.filter(quantity__gte=1, quantity__lt=3)
        elif self.value() == '3-5':
            return queryset.filter(quantity__gte=3, quantity__lt=5)
        elif self.value() == '5-10':
            return queryset.filter(quantity__gte=5, quantity__lt=10)
        elif self.value() == '10+':
            return queryset.filter(quantity__gte=10)
        return queryset

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cartItem_id', 'user', 'get_user_first_name', 'get_user_last_name', 'pro', 'quantity', 'product_image')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'pro__proName', 'quantity')
    list_filter = ('user__username', 'pro__proName', QuantityRangeFilter)

    def get_user_first_name(self, obj):
        return obj.user.first_name
    get_user_first_name.short_description = 'User First Name'

    def get_user_last_name(self, obj):
        return obj.user.last_name
    get_user_last_name.short_description = 'User Last Name'

    def product_image(self, obj):
        # Lấy hình ảnh đầu tiên liên quan đến sản phẩm
        image = Image.objects.filter(pro=obj.pro).first()
        if image:
            if image.image_file:
                return format_html('<img src="{}" width="60" height="60" />', image.image_file.url)
            elif image.image_url:
                return format_html('<img src="{}" width="60" height="60" />', image.image_url)
        return 'No Image'

    product_image.short_description = 'Product Image'

    product_image.short_description = 'Product Image'

admin.site.register(CartItem, CartItemAdmin)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class InforDeliveryInline(admin.TabularInline):
    model = InforDelivery
    extra = 1

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'receiver_name', 'orderDate', 'orderStatus', 'payment_status', 'payment_method')
    search_fields = ('orderDate', 'user__username', 'orderStatus', 'infordelivery__receiverName', 'payment__paymentStatus', 'payment__payMethod__payName')
    list_filter = ('orderStatus', 'user__username', 'payment__paymentStatus', 'payment__payMethod__payName', ('orderDate', DateFieldListFilter),)
    inlines = [OrderItemInline, InforDeliveryInline, PaymentInline]

    def receiver_name(self, obj):
        infor_delivery = InforDelivery.objects.filter(order=obj).first()
        return infor_delivery.receiverName if infor_delivery else 'No Delivery Info'
    receiver_name.short_description = 'Receiver Name'

    def payment_status(self, obj):
        payment = Payment.objects.filter(order=obj).first()
        return payment.paymentStatus if payment else 'No Payment Info'
    payment_status.short_description = 'Payment Status'

    def payment_method(self, obj):
        payment = Payment.objects.filter(order=obj).first()
        return payment.payMethod.payName if payment else 'No Payment Info'
    payment_method.short_description = 'Payment Method'

admin.site.register(Order, OrderAdmin)

# class InforDeliveryAdmin(admin.ModelAdmin):
#     list_display = ('inforDeli_id', 'receiverName', 'province', 'district', 'street', 'phoneNumber')
#     search_fields = ('receiverName', 'province', 'district', 'street', 'phoneNumber')

# admin.site.register(InforDelivery, InforDeliveryAdmin)

# class PaymentStatusFilter(admin.SimpleListFilter):
#     title = 'Payment Status'
#     parameter_name = 'payment_status'

#     def lookups(self, request, model_admin):
#         return (
#             ('unpaid', 'Unpaid'),
#             ('refunded', 'Refunded'),
#             ('paid', 'Paid'),
#         )

#     def queryset(self, request, queryset):
#         if self.value() == 'unpaid':
#             return queryset.filter(paymentStatus='unpaid')
#         elif self.value() == 'refunded':
#             return queryset.filter(paymentStatus='refunded')
#         elif self.value() == 'paid':
#             return queryset.filter(paymentStatus='paid')

# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('payment_id', 'paymentDate', 'paymentStatus', 'payMethod')
#     search_fields = ('paymentDate', 'paymentStatus', 'payMethod__payName')
#     list_filter = ('payMethod__payName', PaymentStatusFilter)

#     def formfield_for_choice_field(self, db_field, request, **kwargs):
#         if db_field.name == 'paymentStatus':
#             kwargs['choices'] = (
#                 ('unpaid', 'Unpaid'),
#                 ('refunded', 'Refunded'),
#                 ('paid', 'Paid'),
#             )
#         return super().formfield_for_choice_field(db_field, request, **kwargs)

# admin.site.register(Payment, PaymentAdmin)

class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('payMethod_id', 'payName', 'description', 'display_image')
    search_fields = ('payName', 'description')

    def display_image(self, obj):
        if obj.payImage:
            return format_html('<img src="{}" width="60" height="60" />', obj.payImage.url)
        return 'No Image'
    display_image.short_description = 'Image'

admin.site.register(PaymentMethod, PaymentMethodAdmin)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('rate_id', 'user', 'pro', 'content', 'product_image')
    search_fields = ('user__username', 'pro__proName', 'content')
    list_filter = ('user__username', 'pro__proName')

    def product_image(self, obj):
        # Lấy hình ảnh đầu tiên liên quan đến sản phẩm
        image = Image.objects.filter(pro=obj.pro).first()
        if image:
            if image.image_file:
                return format_html('<img src="{}" width="60" height="60" />', image.image_file.url)
            elif image.image_url:
                return format_html('<img src="{}" width="60" height="60" />', image.image_url)
        return 'No Image'

    product_image.short_description = 'Product Image'

admin.site.register(Rating, RatingAdmin)