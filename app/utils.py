import json
from app import db
import os
from app import model
from app.model import Category, Product, User, UserRole, Receipt, ReceiptDetail
from app import app
import hashlib
from flask_login import login_user
from sqlalchemy import func

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)

def load_categories():
    return Category.query.all()

def load_products(cate_id=None, keyword=None, from_price=None, to_price=None,page=1):
    products = Product.query.filter(Product.active.__eq__(True))           #equal so sanh

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))
    if keyword:
        products = products.filter(Product.name.contains(keyword))
    if from_price:
        products = products.filter(Product.price.__ge__(from_price))
    if to_price:
        products = products.filter(Product.price.__le__(to_price))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size

    return products.slice(start, start+page_size).all()


def register_user(name, username, password, email=None, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=email.strip() if email else email,
                avatar=avatar)
    db.session.add(user)

    try:
        db.session.commit()
    except:
        return False
    else:
        return True

def count_products():
    return Product.query.filter(Product.active.__eq__(True)).count()

def get_productID(product_id):
    return Product.query.get(product_id)

def get_user_by_id(user_id):
    return User.query.get(user_id)

def check_user_login(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()

def category_stats():
    return db.session.query(Category.id, Category.name, func.count(Product.id)).\
                      join(Product, Category.id.__eq__(Product.category_id), isouter=True).\
                      group_by(Category.id, Category.name).all()

def product_stats(kw=None, from_date=None, to_date=None):
    q = db.session.query(Product.id, Product.name).join(ReceiptDE)

    return  q
