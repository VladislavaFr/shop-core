import json
from abc import ABC, abstractmethod


# Абстрактный базовый класс
class BaseProduct(ABC):
    """
    Абстрактный базовый класс для всех продуктов.
    Определяет интерфейс, который должны реализовать все продукты.
    """

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @property
    @abstractmethod
    def price(self):
        pass

    @price.setter
    @abstractmethod
    def price(self, value):
        pass

    @abstractmethod
    def __str__(self):
        pass


# Миксин для логирования создания объектов
class CreationLoggerMixin:
    """Миксин, который печатает информацию о создании объекта."""

    def __init__(self, *args, **kwargs):
        class_name = self.__class__.__name__
        print(f"[Создан объект] Класс: {class_name}, аргументы: {args}, именованные: {kwargs}")
        super().__init__(*args, **kwargs)


# Класс Product
class Product(CreationLoggerMixin, BaseProduct):
    """
    Класс продукта для интернет-магазина.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        super().__init__(name, description, price if price > 0 else 0, quantity)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif new_price < self._price:
            confirm = input(f"Вы понижаете цену с {self._price} до {new_price}. Подтвердить? (y/n) ")
            if confirm.lower() == "y":
                self._price = new_price
        else:
            self._price = new_price

    @classmethod
    def new_product(cls, product_dict: dict, existing_products=None):
        if existing_products is None:
            existing_products = []
        for p in existing_products:
            if p.name == product_dict["name"]:
                p.quantity += product_dict["quantity"]
                p.price = max(p.price, product_dict["price"])
                return p
        return cls(**product_dict)

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError("Можно складывать только объекты одного класса")
        return self.price * self.quantity + other.price * other.quantity


# Класс Category
class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products=None):
        self.name = name
        self.description = description
        self._products = products if products else []
        Category.category_count += 1
        Category.product_count += len(self._products)

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product или его наследников")
        self._products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        return "\n".join(str(p) for p in self._products)

    def __str__(self):
        total_quantity = sum(p.quantity for p in self._products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


# Классы-наследники
class Smartphone(Product):
    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


# Итератор по категории
class CategoryIterator:
    def __init__(self, category):
        self._products = category._products
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._products):
            raise StopIteration
        product = self._products[self._index]
        self._index += 1
        return product


# Загрузка данных из JSON
def load_products_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    categories = []
    for cat_data in data:
        products = [Product.new_product(prod) for prod in cat_data["products"]]
        category = Category(cat_data["name"], cat_data["description"], products)
        categories.append(category)
    return categories


# Пример использования
if __name__ == "__main__":
    p1 = Product("Кофе", "Арабика", 250, 10)
    p2 = Smartphone("iPhone", "Смартфон", 120000, 5, 95, "14 Pro", 256, "черный")
    p3 = LawnGrass("Газон", "Трава", 500, 20, "Голландия", 7, "зеленый")

    cat1 = Category("Напитки", "Разные напитки")
    cat2 = Category("Электроника", "Разная электроника")
    cat3 = Category("Сад", "Товары для сада")

    cat1.add_product(p1)
    cat2.add_product(p2)
    cat3.add_product(p3)

    print(cat1)
    print(cat1.products)
    print(cat2)
    print(cat2.products)

    