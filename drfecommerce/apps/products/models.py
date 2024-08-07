from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from drfecommerce.apps.products.fields import OrderField


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    is_active = models.BooleanField(default=False)
    parent = TreeForeignKey(to='self', on_delete=models.PROTECT, null=True, blank=True, related_name='children')

    objects = models.Manager()
    active_objects = ActiveManager()

    class Meta:
        verbose_name_plural = 'Categories'

    class MPPTMeta:
        order_insertion_by = ['name']

    def __str__(self) -> str:
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        self.slug = self.name.replace(' ', '-').lower()
        super().save()


class Brand(models.Model):
    name = models.CharField(max_length=120, unique=True)
    is_active = models.BooleanField(default=False)

    objects = models.Manager()
    active_objects = ActiveManager()

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(to=Brand, on_delete=models.PROTECT)
    category = TreeForeignKey(to=Category, null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()

    def __str__(self) -> str:
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        self.slug = self.name.replace(' ', '-').lower()
        super(Product, self).save()


class ProductLine(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100)
    stock_quantity = models.PositiveIntegerField()
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='product_lines')
    order = OrderField(unique_for_field='product', blank=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()

    def __str__(self) -> str:
        return f'Name: {self.product.name} | SKU: {self.sku}'

    def clean(self):
        queryset = ProductLine.objects.filter(product=self.product)
        for obj in queryset:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError('Order must be unique for each product.')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)


class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=120, blank=True)
    url = models.ImageField(upload_to='products_images/', default='/images/default.jpg')
    product_line = models.ForeignKey(to=ProductLine, on_delete=models.CASCADE, related_name='product_images')
    order = OrderField(unique_for_field='product_line', blank=True)

    def __str__(self):
        return f'Product Line: {self.product_line.sku} | Name: {self.url}'
