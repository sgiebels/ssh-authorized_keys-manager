# #ModuleNotFoundError: No module named 'flask_sqlalchemy'
# $ poetry add flask_sqlalchemy
# $ poetry run python3 join.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
	client_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	phone = db.Column(db.Integer)

class Order(db.Model):
	order_id = db.Column(db.Integer, primary_key=True)
	client_id = db.Column(db.String(50), db.ForeignKey('clients.client_id'))
	invoice = db.Column(db.Integer)

results = db.session.query(Client, Order).join(Order).all()

#Printing the results:
for client, order in results:
	print(client.name, order.order_id)
