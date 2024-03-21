# mypackage/__init__.py

from flask import Flask

from resources import create_app
from resources.extensions import db


app = create_app()


class ProcessDate(db.Model):
    __tablename__ = 'process_date'
    id = db.Column(db.Integer, primary_key=True)
    information_date = db.Column(db.String(20), unique=True)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    commodity = db.Column(db.String(50))
    product_sales = db.relationship(
        'ProductSales', backref='products', lazy=True)


class Container(db.Model):
    __tablename__ = 'containers'

    id = db.Column(db.Integer, primary_key=True)
    container = db.Column(db.String(50))
    container_sales = db.relationship(
        'ProductSales', backref='containers', lazy=True)


class ProductCombination(db.Model):
    __tablename__ = 'combinations'

    id = db.Column(db.Integer, primary_key=True)
    combination = db.Column(db.String(50))
    combination_sales = db.relationship(
        'ProductSales', backref='combinations', lazy=True)


class ProductSales(db.Model):
    __tablename__ = 'product_sales'

    id = db.Column(db.Integer, primary_key=True)
    information_date = db.Column(db.String(20))
    commodity_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    container_id = db.Column(db.Integer, db.ForeignKey('containers.id'))
    combination_id = db.Column(db.Integer, db.ForeignKey('combinations.id'))
    total_value_sold = db.Column(db.Float)
    total_quantity_sold = db.Column(db.Integer)
    total_kg_sold = db.Column(db.Float)


with app.app_context():
    db.create_all()
