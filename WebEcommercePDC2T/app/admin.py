from django.contrib import admin
from django.utils.html import format_html
from .models import Brand, Category, Product, Image

class BrandAdmin(admin.ModelAdmin):
    list_display = ('bra_id', 'braName', 'display_image')

    def display_image(self, obj):
        if obj.braImage:
            return format_html('<img src="{}" width="50" height="50" />', obj.braImage.url)
        return 'No Image'
    display_image.short_description = 'Image'

admin.site.register(Brand, BrandAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cate_id', 'cateName', 'cateWarranty')
admin.site.register(Category, CategoryAdmin)

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('pro_id', 'proName', 'proDescription', 'proPrice', 'get_brand_name', 'get_category_name', 'proManufature', 'display_image')
    inlines = [ImageInline]

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
                return format_html('<img src="{}" width="50" height="50" />', image.image_file.url)
            elif image.image_url:
                return format_html('<img src="{}" width="50" height="50" />', image.image_url)
        return 'No Image'
    display_image.short_description = 'Image'

admin.site.register(Product, ProductAdmin)