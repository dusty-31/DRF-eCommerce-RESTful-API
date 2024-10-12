# Generated by Django 5.0.6 on 2024-10-12 20:34

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models

import drfecommerce.apps.products.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Attribute',
                'verbose_name_plural': 'Attributes',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=120)),
                (
                    'attribute',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='attribute_values',
                        to='products.attribute',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Attribute Value',
                'verbose_name_plural': 'Attribute Values',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                (
                    'parent',
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='children',
                        to='products.category',
                    ),
                ),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('description', models.TextField(blank=True)),
                ('is_digital', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.brand')),
                (
                    'category',
                    mptt.fields.TreeForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category'
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='ProductLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sku', models.CharField(max_length=100)),
                ('stock_quantity', models.PositiveIntegerField()),
                ('order', drfecommerce.apps.products.fields.OrderField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                (
                    'product',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name='product_lines', to='products.product'
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternative_text', models.CharField(blank=True, max_length=120)),
                ('url', models.ImageField(default='/images/default.jpg', upload_to='products_images/')),
                ('order', drfecommerce.apps.products.fields.OrderField(blank=True)),
                (
                    'product_line',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='product_images',
                        to='products.productline',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='ProductLineAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'attribute_value',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='attribute_values_av',
                        to='products.attributevalue',
                    ),
                ),
                (
                    'product_line',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='attribute_values_pl',
                        to='products.productline',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Product Line Attribute Value',
                'verbose_name_plural': 'Product Line Attribute Values',
                'unique_together': {('attribute_value', 'product_line')},
            },
        ),
        migrations.AddField(
            model_name='productline',
            name='attribute_values',
            field=models.ManyToManyField(
                related_name='product_lines', through='products.ProductLineAttributeValue', to='products.attributevalue'
            ),
        ),
    ]
