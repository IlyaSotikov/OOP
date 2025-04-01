class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"Product(name={self.name}, price={self.price})"

    def __repr__(self):
        return f"Product({self.name!r}, {self.price!r})"

products_1d = [
    Product("Apple", 100),
    Product("Banana", 50),
    Product("Kivi", 75)
]

print("Одномерный список:")
for product in products_1d:
    print(product)

products_2d = [
    [Product("Laptop", 1000), Product("Mouse", 500)],
    [Product("Keyboard", 700), Product("Monitor", 1200)],
    [Product("Phone", 800), Product("MK-677", 9000)]
]

print("\nДвумерный список:")
for row in products_2d:
    for product in row:
        print(product)

def find_max_price(products):
    if not products:
        return None

    max_product = None
    max_price = float('-inf')

    for row in products:
        for product in row:
            if product.price > max_price:
                max_price = product.price
                max_product = product

    return max_product

max_product = find_max_price(products_2d)
print(f"\nОбъект с максимальной ценой: {max_product}")
