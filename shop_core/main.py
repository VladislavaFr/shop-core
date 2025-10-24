import json
from typing import List, Optional


class Product:
    """Класс продукта интернет-магазина с приватной ценой и методами геттера/сеттера."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self._price = float(price)  # приватный атрибут
        self.quantity = int(quantity)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price: float):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        if new_price < self._price:
            confirm = input(f"Цена товара {self.name} снижается с {self._price} до {new_price}. Подтверждаете? y/n: ")
            if confirm.lower() != 'y':
                print("Действие отменено")
                return
        self._price = new_price

    @classmethod
    def new_product(cls, data: dict, products_list: Optional[List['Product']] = None):
        """
        Создаёт новый объект Product на основе словаря.
        Если продукт с таким именем уже есть в списке products_list, объединяет количество и выбирает максимальную цену.
        """
        name = data["name"]
        description = data.get("description", "")
        price = float(data["price"])
        quantity = int(data["quantity"])

        if products_list:
            for prod in products_list:
                if prod.name == name:
                    prod.quantity += quantity
                    if price > prod.price:
                        prod.price = price
                    return prod

        return cls(name, description, price, quantity)


class Category:
    """Класс категории товаров с приватным списком товаров."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None):
        self.name = name
        self.description = description
        self._products = products if products else []

        Category.category_count += 1
        Category.product_count += len(self._products)

    def add_product(self, product: Product):
        """Добавляет продукт в категорию."""
        self._products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает все продукты как строки."""
        result = ""
        for p in self._products:
            result += f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт.\n"
        return result


def load_categories_from_json(file_path: str) -> List[Category]:
    """
    Загружает категории и продукты из JSON файла.
    Формат JSON:
    [
        {
            "name": "Категория",
            "description": "Описание",
            "products": [
                {"name": "Продукт", "description": "Описание", "price": 100, "quantity": 2},
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
        products = [Product.new_product(prod) for prod in cat_data.get("products", [])]
        category = Category(cat_data["name"], cat_data.get("description", ""), products)
        categories.append(category)
    return categories


if __name__ == "__main__":
    # Пример инициализации продуктов
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Смартфоны с расширенным функционалом", [product1, product2, product3])
    print(category1.products)

    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category2 = Category("Телевизоры", "Современные телевизоры", [product4])
    print(category2.products)

    # Пример добавления нового продукта
    new_prod = Product.new_product({"name": "Iphone 15", "description": "512GB", "price": 220000, "quantity": 2},
                                   products_list=category1._products)
    category1.add_product(new_prod)
    print(category1.products)
