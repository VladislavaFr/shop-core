import json
import pytest
from shop_core.main import Product, Category, load_categories_from_json


@pytest.fixture(autouse=True)
def reset_counters():
    """Сбрасываем счетчики перед каждым тестом."""
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


def test_category_init_and_counts():
    p1 = Product("P1", "D1", 1.0, 1)
    p2 = Product("P2", "D2", 2.0, 2)
    cat = Category("Cat", "Description", [p1, p2])

    assert cat.name == "Cat"
    assert cat.description == "Description"
    assert len(cat.products) == 2
    assert Category.category_count == 1
    assert Category.product_count == 2


def test_multiple_categories_counts():
    p1 = Product("P1", "D1", 1.0, 1)
    p2 = Product("P2", "D2", 2.0, 2)
    p3 = Product("P3", "D3", 3.0, 3)

    Category("C1", "D1", [p1])
    Category("C2", "D2", [p2, p3])

    assert Category.category_count == 2
    assert Category.product_count == 3


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
    assert cats[0].name == "TestCat"
    assert len(cats[0].products) == 2
    assert Category.category_count == 1
    assert Category.product_count == 2
