from flask import Flask, jsonify, request
from dataclasses import dataclass, asdict
from typing import List

app = Flask(__name__)


@dataclass
class Product:
    id: int
    name: str
    category: str
    price: float
    stock: int


class ProductService:

    def __init__(self):
        self.products: List[Product] = [
            Product(1, "Keyboard", "Accessories", 45.99, 18),
            Product(2, "Mouse", "Accessories", 24.50, 30),
            Product(3, "Monitor", "Displays", 259.90, 12)
        ]
        self.next_id = 4

    def get_all(self):
        return [asdict(product) for product in self.products]

    def get_by_id(self, product_id):
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def create(self, data):
        product = Product(
            self.next_id,
            data["name"],
            data["category"],
            float(data["price"]),
            int(data["stock"])
        )

        self.products.append(product)
        self.next_id += 1
        return asdict(product)

    def update(self, product_id, data):
        product = self.get_by_id(product_id)

        if not product:
            return None

        product.name = data.get("name", product.name)
        product.category = data.get("category", product.category)
        product.price = float(data.get("price", product.price))
        product.stock = int(data.get("stock", product.stock))

        return asdict(product)

    def delete(self, product_id):
        product = self.get_by_id(product_id)

        if not product:
            return False

        self.products.remove(product)
        return True


service = ProductService()


@app.get("/products")
def products():
    return jsonify(service.get_all())


@app.get("/products/<int:product_id>")
def product(product_id):
    product = service.get_by_id(product_id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify(asdict(product))


@app.post("/products")
def create_product():
    data = request.get_json()

    required = ["name", "category", "price", "stock"]

    if not all(field in data for field in required):
        return jsonify({"message": "Invalid request"}), 400

    product = service.create(data)

    return jsonify(product), 201


@app.put("/products/<int:product_id>")
def update_product(product_id):
    data = request.get_json()

    product = service.update(product_id, data)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify(product)


@app.delete("/products/<int:product_id>")
def delete_product(product_id):
    if not service.delete(product_id):
        return jsonify({"message": "Product not found"}), 404

    return jsonify({"message": "Product deleted"})


if __name__ == "__main__":
    app.run(debug=True)
