"""
Протестируйте классы из модуля homework/models.py
"""
import pytest
from eshop.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        assert product.check_quantity(product.quantity - 1)

    def test_product_check_quantity_more_than_available(self, product):
        assert not product.check_quantity(product.quantity + 1)

    def test_buy_product(self, product):
        quantity_of_purchased_goods = 1
        products_before_purchase = product.quantity
        assert product.buy(quantity_of_purchased_goods) == products_before_purchase - quantity_of_purchased_goods

    def test_buy_product_more_than_available(self, product):
        with pytest.raises(ValueError):
            assert product.buy(product.quantity + 1)


class TestCart:

    def test_add_new_product(self, cart, product):
        cart.add_product(product, 1)
        assert cart.products[product] == 1

    def test_add_an_existing_product(self, cart, product):
        cart.add_product(product, 1)
        cart.add_product(product, 2)
        assert cart.products[product] == 3

    def test_partial_remove_product(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 3)
        assert cart.products[product] == 2

    def test_total_remove_product(self, cart, product):
        cart.add_product(product, 2)
        cart.remove_product(product)
        assert len(cart.products) == 0

    def test_total_remove_product_with_more_than_available_value(self, cart, product):
        cart.add_product(product, 2)
        cart.remove_product(product, 3)
        assert len(cart.products) == 0

    def test_clear_cart(self, cart, product):
        cart.add_product(product, 5)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price_from_non_empty_cart(self, cart, product):
        quantity_of_purchased_goods = 3
        total_price = quantity_of_purchased_goods * product.price
        cart.add_product(product, quantity_of_purchased_goods)
        assert cart.get_total_price() == total_price

    def test_get_total_price_from_empty_cart(self, cart, product):
        assert cart.get_total_price() == 0

    def test_buy(self, cart, product):
        products_before_purchase = product.quantity
        cart.add_product(product, 3)
        cart.buy()
        assert product.quantity == products_before_purchase - 3

    def test_buy_more_than_available(self, cart, product):
        cart.add_product(product, product.quantity + 1)
        with pytest.raises(ValueError):
            cart.buy()
