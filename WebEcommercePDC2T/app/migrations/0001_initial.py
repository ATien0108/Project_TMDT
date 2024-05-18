# Generated by Django 5.0.4 on 2024-05-18 16:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('blog_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('blogTitle', models.CharField(max_length=255)),
                ('blogContent', models.TextField()),
                ('blogDate', models.DateField()),
                ('image_file', models.ImageField(blank=True, null=True, upload_to='blog_images/')),
                ('image_url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('bra_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('braName', models.CharField(max_length=100)),
                ('braImage', models.ImageField(blank=True, null=True, upload_to='brand_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('cate_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cateName', models.CharField(max_length=255)),
                ('cateWarranty', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('payMethod_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('payName', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlogDetails',
            fields=[
                ('blogDel_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('blogDelTitle', models.CharField(max_length=255)),
                ('image_file', models.ImageField(blank=True, null=True, upload_to='blog_details_images/')),
                ('image_url', models.URLField(blank=True, null=True)),
                ('description', models.TextField()),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='app.blog')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('orderDate', models.DateField()),
                ('orderStatus', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('return', 'Return'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InforDelivery',
            fields=[
                ('inforDeli_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('receiverName', models.CharField(max_length=255)),
                ('province', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('phoneNumber', models.CharField(max_length=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.order')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('paymentDate', models.DateField()),
                ('paymentStatus', models.CharField(choices=[('unpaid', 'Unpaid'), ('refunded', 'Refunded'), ('paid', 'Paid')], max_length=255)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.order')),
                ('payMethod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.paymentmethod')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('pro_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('proName', models.CharField(max_length=255)),
                ('proDescription', models.TextField()),
                ('proPrice', models.FloatField()),
                ('proManufature', models.IntegerField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.brand')),
                ('cate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('orderItem_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('proPrice', models.FloatField()),
                ('proQuantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.order')),
                ('pro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('img_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('image_file', models.ImageField(blank=True, null=True, upload_to='product_images/')),
                ('image_url', models.URLField(blank=True, null=True)),
                ('pro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('cartItem_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSpecification',
            fields=[
                ('prod_spec_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('spec', models.CharField(blank=True, max_length=255, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('rate_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('pro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
