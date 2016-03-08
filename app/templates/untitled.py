from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test1.db'
db = SQLAlchemy(app)

class Items(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Naming = db.Column(db.String(80))
	Description = db.Column(db.String)
	Cat_id = db.Column(db.Integer, db.ForeignKey('Cat.id'))
	Cat= db.relationship('Cat',
		backref=db.backref('category_items', lazy='dynamic'))
	def __init__(self, Naming, Description,Categoriess):
		self.Naming = Naming
		self.Description = Description
		self.Categoriess=Categoriess


class Cat(db.Model):
	__tablename__ ='Cat'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	def __init__(self, name):
		self.name = name