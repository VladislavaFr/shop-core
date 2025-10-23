import pytest
from shop_core.main import Product, Category


@pytest.fixture(autouse=True)
def reset_counters():
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


def test_product_init():
    p = Product("Test", "Desc", 10.5, 3)
    assert p.name == "Test"
    assert p.description == "Desc"
    assert p.price == 10.5
    assert p.quantity == 3


def test_category_init_and_counts():
    p1 = Product("P1", "D1", 1.0, 1)
    p2 = Product("P2", "D2", 2.0, 2)
    cat = Category("Cat", "Desc", [p1, p2])
    assert cat.name == "Cat"
    assert len(cat._products) == 2
    assert Category.category_count == 1
    assert Category.product_count == 2


def test_add_product_and_getter():
    cat = Category("Cat", "Desc")
    p = Product("New", "Desc", 5.0, 1)
    cat.add_product(p)
    assert "New, 5.0 руб. Остаток: 1 шт." in cat.products
    assert Category.product_count == 1


def test_product_price_setter(monkeypatch):
    p = Product("P", "Desc", 100, 1)
    # Тест отрицательной цены
    p.price = -10
    assert p.price == 100
    # Тест понижения цены с подтверждением
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    p.price = 50
    assert p.price == 100  # действие отменено
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    p.price = 50
    assert p.price == 50


def test_new_product_and_duplicates():
    p_list = [Product("A", "D", 10, 1)]
    new = Product.new_product({"name": "A", "description": "D2", "price": 20, "quantity": 2}, p_list)
    assert new.quantity == 3
    assert new.price == 20
