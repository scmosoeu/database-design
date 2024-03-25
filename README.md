# database-design

Database normalization to star or snowflake format

The relational database is created using using flask and flask-sqlalchemy ensuring the 

```bash
pip install flask
pip install flask-sqlalchemy
```

![Data model](imgs/data_model.PNG)

```python
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
```