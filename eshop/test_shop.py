"""
Протестируйте классы из модуля homework/models.py
"""
import pytest
from eshop.models import Product, Cart


@pytest.fixture
def first_product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def second_product():
    return Product("pencil", 20, "This is a pencil", 3)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity_less_then_available(self, first_product):
        assert first_product.check_quantity(first_product.quantity - 1)

    def test_product_check_quantity_with_equals_value(self, first_product):
        assert first_product.check_quantity(first_product.quantity)

    def test_product_check_quantity_more_than_available(self, first_product):
        assert not first_product.check_quantity(first_product.quantity + 1)

    def test_buy_product_less_than_available(self, first_product):
        assert first_product.buy(first_product.quantity - 1)

    def test_buy_product_with_equals_quantity(self, first_product):
        assert first_product.buy(first_product.quantity)

    def test_buy_product_more_than_available(self, first_product):
        with pytest.raises(ValueError):
            assert first_product.buy(first_product.quantity + 1)


class TestCart:

    def test_add_new_product(self, cart, first_product, second_product):
        cart.add_product(first_product, 1)
        cart.add_product(second_product, 2)
        assert cart.products[first_product] == 1
        assert cart.products[second_product] == 2

    def test_add_an_existing_product(self, cart, first_product, second_product):
        cart.add_product(first_product, 1)
        cart.add_product(first_product, 2)
        cart.add_product(second_product,4)
        cart.add_product(second_product,2)
        assert cart.products[first_product] == 3
        assert cart.products[second_product] == 6

    def test_partial_remove_product(self, cart, first_product, second_product):
        cart.add_product(first_product, 5)
        cart.add_product(second_product, 2)
        cart.remove_product(first_product, 3)
        cart.remove_product(second_product, 1)
        assert cart.products[first_product] == 2
        assert cart.products[second_product] == 1

    def test_remove_all_product_with_equals_value(self, cart, first_product):
        cart.add_product(first_product, 5)
        cart.remove_product(first_product,5)
        assert len(cart.products) == 0
    def test_total_remove_product(self, cart, first_product):
        cart.add_product(first_product, 2)
        cart.remove_product(first_product)
        assert len(cart.products) == 0

    def test_total_remove_product_with_more_than_available_value(self, cart, first_product):
        cart.add_product(first_product, 2)
        cart.remove_product(first_product, 3)
        assert len(cart.products) == 0

    def test_clear_cart(self, cart, first_product):
        cart.add_product(first_product, 5)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price_from_non_empty_cart(self, cart, first_product):
        quantity_of_purchased_goods = 3
        total_price = quantity_of_purchased_goods * first_product.price
        cart.add_product(first_product, quantity_of_purchased_goods)
        assert cart.get_total_price() == total_price

    def test_get_total_price_from_empty_cart(self, cart, first_product):
        assert cart.get_total_price() == 0

    def test_buy(self, cart, first_product, second_product):
        products_before_purchase = first_product.quantity
        cart.add_product(first_product, 3)
        cart.add_product(second_product, 3)
        cart.buy()
        assert first_product.quantity == products_before_purchase - 3
        assert second_product.quantity == 0

    def test_buy_when_one_items_quantity_is_more_than_available(self, cart, first_product, second_product):
        cart.add_product(first_product, first_product.quantity + 1)
        cart.add_product(second_product, second_product.quantity - 1)
        with pytest.raises(ValueError):
            cart.buy()
