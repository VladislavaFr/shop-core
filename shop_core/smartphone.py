from shop_core.product import Product

class Smartphone(Product):
    def __init__(self, name, description, price, quantity, brand, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.brand = brand
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self):
        return f"{self.brand} {self.model} ({self.memory}GB, {self.color}) — {self.price} руб."
