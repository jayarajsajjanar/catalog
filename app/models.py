from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test1.db'
db = SQLAlchemy(app)
manager = APIManager(app, flask_sqlalchemy_db=db)




class Items(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Naming = db.Column(db.String(80))
	Description = db.Column(db.String)
	Cat_id = db.Column(db.Integer, db.ForeignKey('Cat.id'))
	Cat= db.relationship('Cat',
		backref=db.backref('its_items', lazy='dynamic'))

	@property
	def serialize(self):
		return {'id': self.id,'Naming': (self.Naming),'Description':self.Description,'Cat_id':self.Cat_id}

	def __init__(self, Naming, Description,Categoriess):
		self.Naming = Naming
		self.Description = Description
		self.Cat=Categoriess


class Cat(db.Model):
	__tablename__ ='Cat'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	items=db.relationship("Items",cascade="save-update, merge, delete")

	@property
	def serialize(self):
		outer=[]
		inner={}

		for k in self.its_items:
			inner = {"Item_ID":k.id,"Name":k.Naming,"Description":k.Description,"Category_ID":k.Cat_id}
			outer.append(inner)

		return {'id': self.id,'name': (self.name),'items':outer}

	def __init__(self, name):
		self.name = name

Items_blueprint = manager.create_api(Items, methods=['GET', 'POST'])
Category_blueprint = manager.create_api(Cat, methods=['GET', 'POST'])