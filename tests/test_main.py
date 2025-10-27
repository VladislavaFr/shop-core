import pytest
from shop_core.main import Product, Category, Smartphone, LawnGrass, CategoryIterator


# Фикстуры для тестов

@pytest.fixture
def product():
    return Product("Кофе", "Арабика", 250, 10)

@pytest.fixture
def smartphone():
    return Smartphone("iPhone", "Смартфон", 120000, 5, 95, "14 Pro", 256, "черный")

@pytest.fixture
def lawn_grass():
    return LawnGrass("Газон", "Трава", 500, 20, "Голландия", 7, "зеленый")

@pytest.fixture
def category(product):
    cat = Category("Напитки", "Разные напитки")
    cat.add_product(product)
    return cat


# Тест инициализации

def test_product_init(product):
    assert product.name == "Кофе"
    assert product.description == "Арабика"
    assert product.price == 250
    assert product.quantity == 10

def test_category_init(category, product):
    assert category.name == "Напитки"
    assert category.description == "Разные напитки"
    assert "Кофе" in category.products


# Тест геттеров/сеттеров цены

def test_product_price_setter(product, monkeypatch):
    # Проверка отрицательной цены
    product.price = -100
    assert product.price == 250  # цена не изменилась

    # Понижение цены с подтверждением 'y'
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    product.price = 200
    assert product.price == 200

    # Понижение цены с отказом 'n'
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    product.price = 100
    assert product.price == 200  # цена не изменилась


# Тест класс-метода new_product

def test_new_product_creation(product):
    new_dict = {"name": "Чай", "description": "Черный чай", "price": 150, "quantity": 5}
    new_prod = Product.new_product(new_dict, existing_products=[product])
    assert new_prod.name == "Чай"
    assert new_prod.price == 150

def test_new_product_update_existing(product):
    new_dict = {"name": "Кофе", "description": "Арабика", "price": 300, "quantity": 5}
    updated_prod = Product.new_product(new_dict, existing_products=[product])
    assert updated_prod.quantity == 15
    assert updated_prod.price == 300


# Тест add_product и проверки типа

def test_add_product_type_error(category):
    with pytest.raises(TypeError):
        category.add_product("не продукт")


# Тест строкового представления

def test_str_methods(product, category):
    assert str(product) == "Кофе, 250 руб. Остаток: 10 шт."
    assert str(category) == "Напитки, количество продуктов: 10 шт."


# Тест магического метода add

def test_add_products(product):
    p2 = Product("Кофе2", "Арабика", 100, 2)
    result = product + p2
    assert result == 250*10 + 100*2

def test_add_type_error(product, smartphone):
    with pytest.raises(TypeError):
        _ = product + smartphone


# Тест наследников

def test_smartphone_attributes(smartphone):
    assert smartphone.efficiency == 95
    assert smartphone.model == "14 Pro"
    assert smartphone.memory == 256
    assert smartphone.color == "черный"

def test_lawngrass_attributes(lawn_grass):
    assert lawn_grass.country == "Голландия"
    assert lawn_grass.germination_period == 7
    assert lawn_grass.color == "зеленый"


# Тест итератора

def test_category_iterator(category):
    iterator = CategoryIterator(category)
    items = [p for p in iterator]
    assert len(items) == 1
    assert items[0].name == "Кофе"


# Тест счетчиков класса Category

def test_category_counters():
    cat1 = Category("A", "Desc")
    cat2 = Category("B", "Desc")
    assert Category.category_count >= 2


# Тест добавления продуктов и подсчет product_count

def test_product_count_reset():
    initial_count = Category.product_count
    c = Category("Test", "Desc")
    p = Product("Test", "Desc", 100, 1)
    c.add_product(p)
    assert Category.product_count == initial_count + 1
