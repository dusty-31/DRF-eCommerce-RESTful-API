import pytest

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    """
    Test the category model.
    """

    def test_str_method(self, category_factory):
        category_object = category_factory()
        assert str(category_object) == category_object.name


class TestBrandModel:
    """
    Test the brand model.
    """

    def test_str_method(self, brand_factory):
        brand_object = brand_factory()
        assert str(brand_object) == brand_object.name


class TestProductModel:
    """
    Test the product model.
    """

    def test_str_method(self, product_factory):
        product_object = product_factory()
        assert str(product_object) == product_object.name
