import json
from typing import List


class Product:
    """Класс продукта интернет-магазина."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = float(price)
        self.quantity = int(quantity)


class Category:
    """Класс категории товаров с подсчётом всех категорий и продуктов."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.products = products

        # обновление атрибутов класса
        Category.category_count += 1
        Category.product_count += len(products)


def load_categories_from_json(file_path: str) -> List[Category]:
    """
    Загрузка категорий и продуктов из JSON файла.
    Формат JSON:
    [
        {
            "name": "Категория 1",
            "description": "Описание категории",
            "products": [
                {"name": "Продукт 1", "description": "Описание", "price": 100, "quantity": 2},
                ...
            ]
        },
        ...
    ]
    """
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    categories = []
    for cat_data in data:
        products = [Product(**prod) for prod in cat_data.get("products", [])]
        category = Category(cat_data["name"], cat_data.get("description", ""), products)
        categories.append(category)
    return categories


if __name__ == "__main__":  # pragma: no cover
    # Пример инициализации продуктов
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(product1.name, product1.price)
    print(product2.name, product2.price)
    print(product3.name, product3.price)

    # Пример инициализации категорий
    category1 = Category(
        "Смартфоны",
        "Смартфоны с расширенным функционалом",
        [product1, product2, product3]
    )
    print(category1.name, len(category1.products))
    print(Category.category_count, Category.product_count)

    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современные телевизоры",
        [product4]
    )
    print(category2.name, len(category2.products))
    print(Category.category_count, Category.product_count)
