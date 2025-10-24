import json
import pytest
from shop_core.main import Product, Category, load_categories_from_json, CategoryIterator


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
    assert isinstance(p.price, float)
    assert p.price == 10.5
    assert p.quantity == 3


def test_product_price_setter(monkeypatch):
    p = Product("P", "D", 10, 1)

    # Проверка отрицательной цены
    p.price = -5
    assert p.price == 10

    # Проверка понижения с отказом
    monkeypatch.setattr("builtins.input", lambda _: "n")
    p.price = 5
    assert p.price == 10

    # Проверка понижения с согласием
    monkeypatch.setattr("builtins.input", lambda _: "y")
    p.price = 5
    assert p.price == 5


def test_category_init_and_counts():
    p1 = Product("P1", "D1", 1.0, 1)
    p2 = Product("P2", "D2", 2.0, 2)
    cat = Category("Cat", "Description", [p1, p2])

    assert cat.name == "Cat"
    assert len(cat.products_list) == 2
    assert Category.category_count == 1
    assert Category.product_count == 2


def test_add_product_and_counts():
    cat = Category("Cat", "Desc")
    p = Product("P", "D", 1.0, 1)
    cat.add_product(p)
    assert len(cat.products_list) == 1
    assert Category.product_count == 1


def test_load_categories_from_json(tmp_path):
    data = [
        {
            "name": "TestCat",
            "description": "desc",
            "products": [
                {"name": "p1", "description": "d1", "price": 10.0, "quantity": 1},
                {"name": "p2", "description": "d2", "price": 20.0, "quantity": 2},
            ],
        }
    ]
    file = tmp_path / "products.json"
    file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    cats = load_categories_from_json(str(file))
    assert len(cats) == 1
    assert len(cats[0].products_list) == 2
    assert Category.category_count == 1
    assert Category.product_count == 2


def test_category_iterator():
    p1 = Product("P1", "D1", 1.0, 1)
    p2 = Product("P2", "D2", 2.0, 2)
    cat = Category("Cat", "Description", [p1, p2])

    iter_cat = CategoryIterator(cat)
    products = [p for p in iter_cat]

    assert len(products) == 2
    assert products[0].name == "P1"
    assert products[1].price == 2.0
