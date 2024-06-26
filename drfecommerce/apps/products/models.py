from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=120, unique=True)
    parent = TreeForeignKey(to='self', on_delete=models.PROTECT, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = 'Categories'

    class MPPTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(to=Brand, on_delete=models.PROTECT)
    category = TreeForeignKey(to=Category, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
