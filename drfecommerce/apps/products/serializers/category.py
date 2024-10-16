from rest_framework import serializers

from drfecommerce.apps.products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
        ]
