from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SelectField
from wtforms.validators import DataRequired

from models import Items
from models import Cat
from models import db

categs = []
for categ_iter in Cat.query.all():
    categs.append((str(categ_iter.id), str(categ_iter.name)))


class form_add_categ(Form):
    categ_name = StringField('categ_name', validators=[DataRequired()])


class form_add_item(Form):
    item_name = StringField('categ_name', validators=[DataRequired()])
    item_desc = StringField('categ_name', validators=[DataRequired()])
    # item_categ = StringField('categ_name', validators=[DataRequired()])
    item_categ = SelectField('State')


class form_edit_item(Form):
    item_name = StringField('categ_name', validators=[DataRequired()])
    item_desc = StringField('categ_name', validators=[DataRequired()])
    # item_categ = StringField('categ_name', validators=[DataRequired()])
    # item_categ = SelectField('State', choices=categs)
