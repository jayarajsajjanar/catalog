
from flask import Flask
# Flask_sqlalchemy is being used - not just "SQLAlchemy"
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# from views import app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test1.db'
db = SQLAlchemy(app)


# Model for items in a category
class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Naming = db.Column(db.String(80))
    Description = db.Column(db.String)
    Cat_id = db.Column(db.Integer, db.ForeignKey('Cat.id'))

    # The items of a category can be accessed by using "Cat_object.its_items"
    Cat = db.relationship('Cat',
                          backref=db.backref('its_items', lazy='dynamic'))

    @property
    def serialize(self):
        return {'id': self.id,
                'Naming': (self.Naming),
                'Description': self.Description,
                'Cat_id': self.Cat_id}

    def __init__(self, Naming, Description, Categoriess):
        self.Naming = Naming
        self.Description = Description
        self.Cat = Categoriess

# Model for Category. It has multiple items. One to many relationship.


class Cat(db.Model):
    # Need to specify table name. ORM doesnt do this for us.
    __tablename__ = 'Cat'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    # Relationship is configured in a way that if a "Category" is deleted,
    # then its associated items are
    # automatically deleted.
    items = db.relationship("Items", cascade="save-update, merge, delete")

    # Below property is used in providing JSON api end point. A datastructure
    # that can be "jsonify" is returned.
    @property
    def serialize(self):
        outer = []
        inner = {}

        for k in self.its_items:
            inner = {"Item_ID": k.id, "Name": k.Naming,
                     "Description": k.Description, "Category_ID": k.Cat_id}
            outer.append(inner)

        return {'id': self.id, 'name': (self.name), 'items': outer}

    def __init__(self, name):
        self.name = name
