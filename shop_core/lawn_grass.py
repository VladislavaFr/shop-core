from shop_core.product import Product

class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, manufacturer, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.manufacturer = manufacturer
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        return f"{self.name} ({self.color}), производитель: {self.manufacturer}, {self.price} руб."
