import json
import os

from app import app

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)

def load_categories():
    return read_json(os.path.join(app.root_path, 'data/categories.json'))

def load_products(cate_id=None, keyword=None, from_price=None, to_price=None):
    products = read_json(os.path.join(app.root_path, 'data/products.json'))

    if cate_id:
        products = [ p for p in products if p['category_id'] == int(cate_id) ]

    if keyword:
        products = [p for p in products if p["name"].lower().find(keyword.lower()) >= 0 ]
    if from_price and to_price:
        products = [p for p in products if p["price"] >= float(from_price) and p["price"] <= float(to_price)]

    return products

def get_productID(product_id):
    product = read_json(os.path.join(app.root_path, 'data/products.json'))
    for p in product:
        if product_id == p["id"]:
            return p
