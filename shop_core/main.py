import json


# Класс Product

class Product:
    """
    Класс продукта для интернет-магазина.

    Атрибуты:
        name (str): Название продукта
        description (str): Описание продукта
        _price (float): Цена продукта (приватный атрибут)
        quantity (int): Количество на складе
    """
    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Инициализация продукта.

        Args:
            name (str): Название продукта
            description (str): Описание продукта
            price (float): Цена продукта
            quantity (int): Количество на складе
        """
        self.name = name
        self.description = description
        self._price = price if price > 0 else 0
        self.quantity = quantity

    @property
    def price(self):
        """
        Геттер для приватного атрибута цены.

        Returns:
            float: Текущая цена продукта
        """
        return self._price

    @price.setter
    def price(self, new_price):
        """
        Сеттер для приватного атрибута цены.
        Проверяет корректность новой цены и при понижении запрашивает подтверждение пользователя.

        Args:
            new_price (float): Новая цена продукта
        """
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
        """
        Класс-метод для создания нового продукта из словаря.
        Если продукт с таким именем уже есть в списке, обновляет количество и цену.

        Args:
            product_dict (dict): Словарь с ключами name, description, price, quantity
            existing_products (list, optional): Список существующих объектов Product

        Returns:
            Product: Новый объект Product или обновленный существующий
        """
        if existing_products is None:
            existing_products = []
        for p in existing_products:
            if p.name == product_dict["name"]:
                p.quantity += product_dict["quantity"]
                p.price = max(p.price, product_dict["price"])
                return p
        return cls(**product_dict)

    def __str__(self):
        """
        Строковое представление продукта.

        Returns:
            str: "Название продукта, X руб. Остаток: X шт."
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """
        Магический метод сложения двух продуктов.
        Складывает только объекты одного класса и возвращает суммарную стоимость.

        Args:
            other (Product): Второй объект для сложения

        Returns:
            float: Сумма произведений цены на количество для двух продуктов

        Raises:
            TypeError: Если объекты разных классов
        """
        if type(self) != type(other):
            raise TypeError("Можно складывать только объекты одного класса")
        return self.price * self.quantity + other.price * other.quantity



# Класс Category

class Category:
    """
    Класс категории товаров.

    Атрибуты класса:
        category_count (int): Общее количество категорий
        product_count (int): Общее количество продуктов во всех категориях
    """
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products=None):
        """
        Инициализация категории.

        Args:
            name (str): Название категории
            description (str): Описание категории
            products (list, optional): Список продуктов в категории
        """
        self.name = name
        self.description = description
        self._products = products if products else []
        Category.category_count += 1
        Category.product_count += len(self._products)

    def add_product(self, product):
        """
        Добавление продукта в категорию.
        Проверяет, что добавляется объект Product или его наследник.

        Args:
            product (Product): Объект продукта для добавления

        Raises:
            TypeError: Если передан не продукт
        """
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product или его наследников")
        self._products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        """
        Геттер для списка продуктов.
        Возвращает строку со всеми продуктами.

        Returns:
            str: Перечень продуктов в формате "__str__" каждого продукта
        """
        return "\n".join(str(p) for p in self._products)

    def __str__(self):
        """
        Строковое представление категории.
        Считает общее количество товаров на складе.

        Returns:
            str: "Название категории, количество продуктов: X шт."
        """
        total_quantity = sum(p.quantity for p in self._products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."



# Классы-наследники

class Smartphone(Product):
    """
    Класс смартфона, наследник Product.

    Атрибуты:
        efficiency (int): Производительность
        model (str): Модель
        memory (int): Объем встроенной памяти
        color (str): Цвет
    """

    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """
    Класс травы газонной, наследник Product.

    Атрибуты:
        country (str): Страна-производитель
        germination_period (int): Срок прорастания
        color (str): Цвет
    """

    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color



# Итератор по категории

class CategoryIterator:
    """
    Итератор по продуктам категории.
    Позволяет перебирать все продукты в цикле for.

    Атрибуты:
        _products (list): Список продуктов категории
        _index (int): Текущий индекс итерации
    """

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
    """
    Загружает категории и продукты из JSON-файла и возвращает список объектов Category.

    Args:
        file_path (str): Путь к JSON-файлу

    Returns:
        list: Список объектов Category
    """
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
    # Создаем продукты
    p1 = Product("Кофе", "Арабика", 250, 10)
    p2 = Smartphone("iPhone", "Смартфон", 120000, 5, 95, "14 Pro", 256, "черный")
    p3 = LawnGrass("Газон", "Трава", 500, 20, "Голландия", 7, "зеленый")

    # Создаем категории
    cat1 = Category("Напитки", "Разные напитки")
    cat2 = Category("Электроника", "Разная электроника")
    cat3 = Category("Сад", "Товары для сада")

    # Добавляем продукты
    cat1.add_product(p1)
    cat2.add_product(p2)
    cat3.add_product(p3)

    # Печатаем
    print(cat1)
    print(cat1.products)
    print(cat2)
    print(cat2.products)

    