from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class form_add_categ(Form):
    categ_name = StringField('categ_name', validators=[DataRequired()])
    