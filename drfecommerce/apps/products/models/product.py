from django.db import models
from mptt.models import TreeForeignKey

from drfecommerce.apps.products.managers import ActiveManager
from drfecommerce.apps.products.models.attribute_value import AttributeValue
from drfecommerce.apps.products.models.category import Category
from drfecommerce.apps.products.models.product_attribute_value import ProductAttributeValue
from drfecommerce.apps.products.models.product_type import ProductType


class Product(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150, unique=True)
    pid = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    category = TreeForeignKey(to=Category, null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    product_type = models.ForeignKey(
        to=ProductType,
        on_delete=models.PROTECT,
        related_name='product_lines',
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    attribute_value = models.ManyToManyField(
        to=AttributeValue,
        through=ProductAttributeValue,
        related_name='product_attr_value',
    )

    objects = models.Manager()
    active_objects = ActiveManager()

    def __str__(self) -> str:
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        self.slug = self.name.replace(' ', '-').lower()
        super(Product, self).save()
