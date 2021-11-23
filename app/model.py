from app import db
from sqlalchemy import Column, Integer, Float, String, Boolean, Enum, ForeignKey, DateTime, Enum
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin
from enum import Enum as UserEnum

class UserRole(UserEnum):
    ADMIN = 1
    USER = 2

class BaseModel(db.Model):
    # chỉ tạo một bảng csdl, không tạo bảng BaseModel
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name

class User(BaseModel, UserMixin):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())

    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name

class Category(BaseModel):
    __tablename__ = "category"

    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name

product_tag = db.Table('product_tag', Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
                       Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True))

class Product(BaseModel):
    __tablename__ = 'product'

    description = Column(String(255))
    price = Column(Float, default=0)
    active = Column(Boolean, default=True)
    image = Column(String(100))
    created_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    tags = relationship('Tag', secondary='product_tag', lazy='subquery', backref=backref('products', lazy=True))

    def __str__(self):
        return self.name

class Tag(BaseModel):
    __tablename__ = 'tag'

    def __str__(self):
        return self.name


# if __name__ == '__main__':
#
#      db.create_all()
#
#     p1 = Product(name='iPhone 7 Plus', description= "Apple, 32GB, RAM: 3GB, iOS13", price=17000000, image="images/iphone11.png", category_id=1)
#     p2 = Product(name='iPad Pro 2020', description="Apple, 128GB, RAM: 6GB", price=37000000, image="images/iphone11.png", category_id=2)
#     p3 = Product(name='Galaxy Note 10 Plus', description="Samsung, 64GB, RAML: 6GB", price=24000000, image="images/iphone11.png", category_id=1)
#
#     db.session.add(p1)
#     db.session.add(p2)
#     db.session.add(p3)
#
#     db.session.commit()





