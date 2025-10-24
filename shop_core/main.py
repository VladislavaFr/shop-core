from shop_core.category import Category
from shop_core.product import Product
from shop_core.smartphone import Smartphone
from shop_core.lawn_grass import LawnGrass


def main():
    # Создание товаров разных категорий
    iphone = Smartphone(
        name="iPhone 15 Pro",
        description="512GB, Gray Space, 2024",
        price=210000.0,
        quantity=8,
        brand="Apple",
        model="15 Pro",
        memory=512,
        color="Серый"
    )

    samsung = Smartphone(
        name="Samsung Galaxy S23 Ultra",
        description="256GB, Серый цвет, 200MP камера",
        price=180000.0,
        quantity=5,
        brand="Samsung",
        model="S23 Ultra",
        memory=256,
        color="Серый"
    )

    grass = LawnGrass(
        name="GreenField Premium",
        description="Трава для газона класса люкс",
        price=2500.0,
        quantity=15,
        manufacturer="GreenCo",
        germination_period="7 дней",
        color="Ярко-зелёная"
    )

    # Создание категорий
    smartphones = Category("Смартфоны", "Современные телефоны премиум-класса")
    garden = Category("Сад", "Товары для благоустройства сада")

    # Добавление товаров
    smartphones.add_product(iphone)
    smartphones.add_product(samsung)
    garden.add_product(grass)

    # Проверка вывода
    print(smartphones)
    print(garden)

    # Проверка сложения одинаковых типов
    total_price = iphone + samsung
    print(f"\nСуммарная стоимость телефонов: {total_price} руб.")

    # Попытка сложить разные типы — вызовет ошибку TypeError
    try:
        _ = iphone + grass
    except TypeError as e:
        print(f"\nОшибка: {e}")

    # Пример неверного добавления в категорию (ожидаем ошибку)
    try:
        smartphones.add_product("не продукт")
    except TypeError as e:
        print(f"\nОшибка при добавлении: {e}")


if __name__ == "__main__":
    main()
