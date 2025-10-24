import json
from typing import List


class Product:
    """Класс продукта интернет-магазина."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self._price = float(price)
        self.quantity = int(quantity)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif value < self._price:
            ans = input(f"Вы хотите понизить цену с {self._price} до {value}? (y/n): ")
            if ans.lower() == "y":
                self._price = value
        else:
            self._price = value

    @classmethod
    def new_product(cls, data: dict, products_list: List['Product'] = None):
        """Создаёт новый объект Product из словаря, проверяет на дубликаты"""
        if products_list:
            for prod in products_list:
                if prod.name == data["name"]:
                    prod.quantity += data["quantity"]
                    if data["price"] > prod.price:
                        prod.price = data["price"]
                    return prod
        return cls(
            data["name"], data["description"], data["price"], data["quantity"]
        )

    def __add__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return (self._price * self.quantity) + (other._price * other.quantity)

    def __str__(self):
        return f"{self.name}, {self._price} руб. Остаток: {self.quantity} шт."


class Category:
    """Класс категории товаров с подсчётом всех категорий и продуктов."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self._products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product):
        self._products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        return "".join([f"{str(prod)}\n" for prod in self._products])

    def __str__(self):
        return f"{self.name}, количество продуктов: {len(self._products)} шт."


class CategoryIterator:
    """Итератор для перебора продуктов категории"""

    def __init__(self, category: Category):
        self._category = category
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._category._products):
            prod = self._category._products[self._index]
            self._index += 1
            return prod
        raise StopIteration


def load_categories_from_json(file_path: str) -> List[Category]:
    """Загрузка категорий и продуктов из JSON файла"""
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    categories = []
    for cat_data in data:
        products = [Product(**prod) for prod in cat_data.get("products", [])]
        category = Category(cat_data["name"], cat_data.get("description", ""), products)
        categories.append(category)
    return categories


if __name__ == "__main__":
    # Примеры использования
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Смартфоны с расширенным функционалом", [product1, product2, product3])
    print(category1)
    print(category1.products)

    # Добавление нового продукта
    product4 = Product("Huawei P60", "128GB", 90000.0, 10)
    category1.add_product(product4)
    print(category1)
    print(category1.products)

    # Итератор
    print("Итератор по товарам:")
    for prod in CategoryIterator(category1):
        print(prod)

    # Проверка сложения продуктов
    total = product1 + product2
    print(f"Сумма стоимости двух продуктов: {total} руб.")
