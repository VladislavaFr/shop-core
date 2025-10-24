from shop_core.product import Product

class Category:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.products = []

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников.")
        self.products.append(product)

    def __str__(self):
        total_quantity = sum(p.quantity for p in self.products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
