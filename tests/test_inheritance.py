import pytest
from shop_core.smartphone import Smartphone
from shop_core.lawn_grass import LawnGrass
from shop_core.category import Category

def test_smartphone_inheritance():
    phone = Smartphone("iPhone", "Описание", 150000, 2, "Apple", "15 Pro", 256, "Silver")
    assert isinstance(phone, Smartphone)
    assert phone.brand == "Apple"
    assert "Apple" in str(phone)

def test_lawn_grass_inheritance():
    grass = LawnGrass("Green", "Трава", 1000, 5, "EcoSeed", "7 дней", "Зелёная")
    assert isinstance(grass, LawnGrass)
    assert grass.manufacturer == "EcoSeed"
    assert "Трава" in grass.description

def test_add_product_only_product():
    category = Category("Тест", "Описание")
    phone = Smartphone("iPhone", "Описание", 1000, 1, "Apple", "15", 256, "White")
    category.add_product(phone)
    assert len(category.products) == 1

    with pytest.raises(TypeError):
        category.add_product("не продукт")
