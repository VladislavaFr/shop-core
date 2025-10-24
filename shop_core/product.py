class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        if price <= 0:
            raise ValueError("Цена должна быть больше нуля.")
        if quantity < 0:
            raise ValueError("Количество не может быть отрицательным.")
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity}"

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных типов.")
        return self.price * self.quantity + other.price * other.quantity
