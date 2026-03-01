# DEFUNCT py code - https://4geeks.com/how-to/sqlalchemy-join
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = "client"
    client_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.Integer)

class Order(db.Model):
    __tablename__ = "order"
    order_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(50), db.ForeignKey('client.client_id'))
    invoice = db.Column(db.Integer)

results = db.session.query(Client, Order).outerjoin(Order).all()

#Printing the results:
for client, order in results:
    print(client.name, order.order_id)

