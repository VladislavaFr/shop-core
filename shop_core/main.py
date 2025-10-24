import json
from typing import List


class Product:
    """Класс продукта интернет-магазина."""

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
        elif new_price < self._price:
            answer = input(
                f"Вы понижаете цену с {self._price} на {new_price}. Согласны? (y/n): "
            )
            if answer.lower() == "y":
                self._price = new_price
        else:
            self._price = new_price

    @classmethod
    def new_product(cls, product_dict: dict, existing_products: List["Product"] = None):
        """
        Создаёт продукт из словаря.
        Доп. задание: объединяет товары с одинаковым именем.
        """
        name = product_dict["name"]
        description = product_dict.get("description", "")
        price = product_dict["price"]
        quantity = product_dict.get("quantity", 1)

        if existing_products:
            for p in existing_products:
                if p.name == name:
                    # объединяем количество и выбираем максимальную цену
                    p.quantity += quantity
                    if price > p.price:
                        p.price = price
                    return p

        return cls(name, description, price, quantity)


class Category:
    """Класс категории товаров с подсчётом всех категорий и продуктов."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product] = None):
        self.name = name
        self.description = description
        self._products = products or []

        Category.category_count += 1
        Category.product_count += len(self._products)

    def add_product(self, product: Product):
        """Добавляет продукт в категорию."""
        self._products.append(product)
        Category.product_count += 1

    @property
    def products_list(self) -> List[Product]:
        """Возвращает список продуктов категории."""
        return self._products

    @property
    def products(self) -> str:
        """Возвращает строку со всеми продуктами."""
        result = ""
        for p in self._products:
            result += f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт.\n"
        return result


def load_categories_from_json(file_path: str) -> List[Category]:
    """Загружает категории и продукты из JSON файла."""
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    categories = []
    for cat_data in data:
        products = [Product(**prod) for prod in cat_data.get("products", [])]
        category = Category(cat_data["name"], cat_data.get("description", ""), products)
        categories.append(category)
    return categories


class CategoryIterator:
    """Итератор для перебора товаров категории."""

    def __init__(self, category: Category):
        self._products = category.products_list
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._products):
            product = self._products[self._index]
            self._index += 1
            return product
        else:
            raise StopIteration


# Пример использования
if __name__ == "__main__":
    p1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    p2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    p3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Смартфоны с расширенным функционалом", [p1, p2, p3])

    # Добавление нового продукта
    p4 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 3)
    category1.add_product(p4)

    print(category1.products)

    # Итерация по продуктам
    for product in CategoryIterator(category1):
        print(product.name, product.price)
