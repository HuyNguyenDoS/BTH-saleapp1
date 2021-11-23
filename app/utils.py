import json
import os
from app import model
from app.model import Category, Product, User
from app import app
import hashlib
from flask_login import login_user

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)

def load_categories():
    return Category.query.all()
    # return read_json(os.path.join(app.root_path, 'data/categories.json'))

def load_products(cate_id=None, keyword=None, from_price=None, to_price=None):
    # products = read_json(os.path.join(app.root_path, 'data/products.json'))
    #
    # if cate_id:
    #     products = [ p for p in products if p['category_id'] == int(cate_id) ]
    #
    # if keyword:
    #     products = [p for p in products if p["name"].lower().find(keyword.lower()) >= 0 ]
    # if from_price and to_price:
    #     products = [p for p in products if p["price"] >= float(from_price) and p["price"] <= float(to_price)]
    #
    # return products
    products = Product.query.filter(Product.active.__eq__(True))           #equal so sanh

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))
    if keyword:
        products = products.filter(Product.name.contains(keyword))
    if from_price:
        products = products.filter(Product.price.__ge__(from_price))
    if to_price:
        products = products.filter(Product.price.__le__(to_price))

    return products.all()

def get_productID(product_id):
    return Product.query.get(product_id)
    # product = read_json(os.path.join(app.root_path, 'data/products.json'))
    # for p in product:
    #     if product_id == p["id"]:
    #         return p

def get_user_by_id(user_id):
    return User.query.get(user_id)

def check_user_login(username, password):
    if username and password:
        pass = hashlib.md5(password.strip().encode('utf-8')).hexdigest()

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.username.__eq__(password).first)